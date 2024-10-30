package main

type Account struct {
	Profile            string `yaml:"profile"`
	AccountID          string `yaml:"account"`
	URL                string `yaml:"url"`
	MFA                string `yaml:"mfa"`
	Role               string `yaml:"role"`
	Region             string `yaml:"region"`
	SkipVerify         bool   `yaml:"skipVerify"`
	AWSSessionDuration string `yaml:"awsSessionDuration"`
}
