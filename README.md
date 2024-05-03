# action-jira-notification

Summary: jira action to create jira problem ticket on job failure.  

![ci](https://github.com/conventional-changelog/standard-version/workflows/ci/badge.svg)
[![version](https://img.shields.io/badge/version-1.x-yellow.svg)](https://semver.org)

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#Features)
* [Assumptions](#Assumptions)
* [Usage](#usage)
* [Project Status](#project-status)

## General Information
- jira action

## Technologies Used
- python script
- GitHub actions

## Features

* using jira jql query api, check if problem ticket already exist
* create problem ticket on failure
* close existing tickets on success

## Assumptions

* jira project has labels enabled on workflow.  This is used to tag and query
* jira project has Done or Resolved status options.

## Usage

* look at examples/jira.yml for usage

## Project Status
Project is: _in_progress_ 