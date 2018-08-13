# codegen

## Problem
Remember how many times you saw some interesting data and wanted to do something even more interesting. Maybe you wanted to create a stock option optimizer and now you need to implement the dumb and tedious part of parsing the JSON. How great of you!

## Solution
Coincidentally, the parsing implementation of such data in different object oriented languages remains the same. Only the semantics change for the most part. Codegen, separates the logic from semantics, implements the logic, but uses templates to derive the semantics representing the logic. It will fetch the json, parse the json, understand the levels of heirarchy in the json, the attributes of each heirarchy, designs classes representing the heirarchies, assigns properties to the class, implements the parsing of said heirarchy along with the logging.

## Usage
python JSONGenerator/generator.py <url_to_json_object> 

## Output
A build folder within the directory of execution will contain the classes generated.
