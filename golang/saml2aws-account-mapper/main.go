package main

import (
	"fmt"
	"os"
	"text/template"

	"gopkg.in/yaml.v3"
)

var (
	accountsFile    string = "accounts.yaml"
	tempateFile     string = "saml2aws.tmpl"
	destinationPath string = fmt.Sprintf("%s/.saml2aws", os.Getenv("HOME"))
)

func main() {
	//Read yaml file
	data, err := os.ReadFile(accountsFile)
	if err != nil {
		panic(fmt.Sprintf("Failed reading file %s", err.Error()))
	}
	//Serialize
	var accounts []Account
	err = yaml.Unmarshal(data, &accounts)
	if err != nil {
		panic(fmt.Sprintf("Failed to unmarshal yaml %s", err.Error()))
	}
	//New template
	tmpl, err := template.ParseFiles(tempateFile)
	if err != nil {
		panic(err)
	}
	// Render template
	file, err := os.OpenFile(destinationPath, os.O_WRONLY, 0644)
	if err != nil {
		panic(err)
	}
	err = tmpl.Execute(file, accounts)
	if err != nil {
		panic(err)
	}
}
