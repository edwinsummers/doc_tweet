# 100DoCtweet

A simple Python script to send daily [#100DaysOfCode](http://www.100daysofcode.com/) status updates. It was developed as a simple project for a #100DaysOfCode effort.

## Usage

From the command line:

`python 100DoCtweet.py <message>`

Example:

`python 100DoCtweet.py 'This is a status update!'`

The application must be registered with Twitter to obtain a 'consumer key' and 'consumer secret', after which you must authenticate to Twitter to allow the application to access your Twitter feed. The application uses OAuth authorization. The application requires read/write permissions but does not have access to your direct messages.

On first run the application will detect that it does not have the necessary authorization tokens and will walk the user through authorization. The resulting credentials file (credentials.json) will be stored in the app directory. The credentials file mask should be set to read-only to the current user by the application. Do not share the credentials file as it contains secret OAuth tokens.

This application has been developed and tested in a Linux environment.