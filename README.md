# Multinational Retail Data Centrialisation

## Table of Contents
1. [Introduction](#introduction)
2. [Installation Instructions](#installation-instructions)
3. [Usage Instructions](#usage-instructions)
4. [File Structure](#file-structure)
5. [License](#license)

## Introduction
This multinational Retail data centralisation project is a comprehensive solution designed to streamline extraction, cleaning and querying data from multiple sources. The goal is to provide a reliable, efficient, and user-friendly tool for organised data storage and usage.

Scenario: You work for a multinational company that sells various goods across the globe. Currently, their sales data is spread across many different data sources making it not easily accessible or analysable by current members of the team. In an effort to become more data-driven, your organisation would like to make its sales data accessible from one centralised location. Your first goal will be to produce a system that stores the current company data in a database so that it's accessed from one centralised location and acts as a single source of truth for sales data. You will then query the database to get up-to-date metrics for the business.

The primary goal of this project is to establish a centralized database system that consolidates the company's sales data, serving as a unified source of truth.

This project extracts data from the following:

AWS RDS database
AWS S3 bucket PDF
AWS S3 bucket CSV
AWS S3 bucket JSON
REST API JSON

## Installation Instructions
Prerequisites: Ensure that you have the necessary pre-installed software ond dependencies installed on your system.

boto3
pandas
python
Requests
SQLAlchemy
tabula_py

clone the Repository: Clone this repository to your local machine using: git clone [repository URL]
Run the application

## Usage Instructions

To run this project, you will have to set up the following credentials and databases:

db_creds.yaml
pgdb_creds.yaml
api_creds.yaml

You should now be able to run the upload scripts to start the data centralisation process. This will intialise the data extraction and cleaning processes, after which the processed data will be uploaded in a central PostgreSQL database.

## File Structure 

data_cleaning.py: This file hosts the 'DataCleaning' class, which encompasses various methods dedicated to purifying and refining data derived from multiple sources.

database_utils.py: In this script, you'll find the 'DatabaseConnector' class. Its primary role is to establish connections and facilitate data uploads to our database system.

data_extraction.py: This script introduces the 'DataExtractor' class, a pivotal utility tool for retrieving data from a diverse array of sources. It includes functionalities for processing data from formats like CSV files, tapping into APIs, and accessing contents stored in an S3 bucket.

## Licence 
MIT License Copyright (c) [2023] [Kian Semnani]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.