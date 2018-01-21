# 100DoCtweet

A simple Python script to send daily [#100DaysOfCode](http://www.100daysofcode.com/) status updates. It was developed as a simple project for a #100DaysOfCode effort.

## Example Usage

From the command line:

`python doctweet.py "*message*"`

`python doctweet.py "This is an example status update!"`

## Setup

Prior to running you must register the application with Twitter to obtain a *consumer key* and *consumer secret* for OAuth authorization. The application will display prompts to guide you through registration. *The application requires read/write permissions in order to send status updates, but does not require access to direct messages.*

On first run or whenever the application cannot find the user preferences file, config.json, it will prompt for the date that the 100DaysOfCode challenge was started as well as a hashtag that you want to send with each tweet (default: #100DaysOfCode). The start date should be entered in ISO notation (YYYY-MM-DD) and is used to calculate a day index prepended to each tweet.

This application has been developed and tested in a Linux environment.
