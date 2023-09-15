package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"os"
	"strings"
	"time"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
	"github.com/aws/aws-sdk-go-v2/service/ec2/types"
	"github.com/gocarina/gocsv"
)

type Tag struct {
	key   string
	value string
}

type Instance struct {
	InstanceId    string `csv:"instance_id"`
	InstanceName  string `csv:"instance_name"`
	InstanceState string `csv:"instance_state"`
	InstanceType  string `csv:"instance_type"`
}

var (
	tags       []Tag
	outputFile string
)

func main() {
	setupAwsLogin()
	flagParse()

	var cancelFn func()
	ctx, cancelFn := context.WithTimeout(context.Background(), time.Second*300)

	if cancelFn != nil {
		defer cancelFn()
	}

	cfg, err := config.LoadDefaultConfig(ctx)
	if err != nil {
		log.Fatalf("unable to load SDK config, %v", err)
	}

	svc := ec2.NewFromConfig(cfg)
	var filters []types.Filter = []types.Filter{}
	for i := range tags {
		tk := fmt.Sprintf("tag:%s", tags[i].key)
		tkp := &tk
		filters = append(filters, types.Filter{
			Name:   tkp,
			Values: []string{tags[i].value}, //TODO: support multiple values
		})
	}

	// dryrun := true
	describeInstancesInput := new(ec2.DescribeInstancesInput)
	*describeInstancesInput = ec2.DescribeInstancesInput{
		// DryRun: &dryrun, TODO: implement dryrun logic
		Filters: filters,
	}
	reservations, err := svc.DescribeInstances(ctx, describeInstancesInput)
	if err != nil {
		panic(err)
	}

	csv, err := os.OpenFile(outputFile, os.O_RDWR|os.O_CREATE, 0755)
	if err != nil {
		panic(err)
	}

	instances := make([]types.Instance, 0)
	for _, r := range reservations.Reservations {
		instances = append(instances, r.Instances...)
	}

	csvinstances := []Instance{}

	for _, i := range instances {
		csvinstances = append(csvinstances, Instance{
			InstanceId:    *i.InstanceId,
			InstanceName:  filterTag(i.Tags, "Name"),
			InstanceState: string(i.State.Name),
			InstanceType:  string(i.InstanceType),
		})
	}

	fmt.Print(csvinstances)
	err = gocsv.MarshalFile(&csvinstances, csv)
	if err != nil {
		panic(err)
	}

	if err := csv.Close(); err != nil {
		log.Fatal(err)
	}
}

func setupAwsLogin() {
	if os.Getenv("AWS_PROFILE") == "" {
		os.Setenv("AWS_PROFILE", "default")
	}

	if os.Getenv("AWS_DEFAULT_REGION") == "" || os.Getenv("AWS_REGION") == "" {
		os.Setenv("AWS_REGION", "us-east-1")
	}

	fmt.Println(os.ExpandEnv("Using AWS_PROFILE $AWS_PROFILE and AWS_REGION $AWS_REGION"))
}

func flagParse() {
	var ts string

	flag.StringVar(&ts, "tags", "", "Tags that will be used to filter the ec2 instances, e.g. key=value;key=value")
	flag.StringVar(&outputFile, "output", "instances.csv", "Output file")
	flag.Parse()

	tags = []Tag{}

	tss := strings.Split(ts, ";")
	for i := range tss {
		key := strings.Split(tss[i], "=")[0]
		value := strings.Split(tss[i], "=")[1]

		tags = append(tags, Tag{key, value})
	}
}

func filterTag(tags []types.Tag, key string) string {
	for _, t := range tags {
		if *t.Key == key {
			return *t.Value
		}
	}

	return ""
}
