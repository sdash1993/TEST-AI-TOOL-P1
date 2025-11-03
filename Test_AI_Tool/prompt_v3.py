from langchain_core.prompts import PromptTemplate

karate_api_prompt = PromptTemplate.from_template(
    """
API End point :-  {endpoint}

Method :- {method_type}

Request Payload :- {payload}
# Karate Test Generation Prompt

## IMPORTANT: Analyze the API First
Before generating tests, analyze:
1. Does the endpoint URL contain query parameters (look for '?' in the endpoint)?
2. Is there a request payload/body?
3. What is the HTTP method?

## Decision Rules for Template Selection:
- If endpoint contains '?' → Use "Helper File Template (with parameters)"
- If endpoint does not contains '?' → Use "Helper File Template (empty request)"
- If payload is empty or null or {{}} → Use "Helper File Template (empty request)"
- If payload exists and no query params → Use appropriate template based on payload complexity


## Task
Generate comprehensive Karate test files for API testing with the following specifications:

## Requirements

### 1. Helper File Must Include:
- DONOT REPLY WITH ANY TEXT OTHER THAN THE REQUIRED FILES
- DONOT REPLY WITH I UNDERSTAND
- DONOT SUPPLY EXPLAINATION IN THE REPLY
- DONOT USE ```gherkin or ``` CODE BLOCKS
- RETURN ONLY THE RAW FEATURE FILE CONTENT
- `@tagName` annotation for the scenario (use `@[apiActionName]` format)
- Background section with Java imports and utility functions if needed
- `Scenario Outline: [API Action] API Helper` as the scenario title
- `mandatoryFields` array with all required parameters including 'tenant'
- `defaultArgs` object with template placeholders: `{{tenant: '<tenant>', field1: '<field1>', field2: '<field2>'}}`
- `fetchArgs(mandatoryFields, defaultArgs)` function call

### CRITICAL: Query Parameter Detection
**BEFORE CHOOSING A TEMPLATE, CHECK:**
- If the endpoint contains '?' followed by parameters (e.g., /api/endpoint?param1=value&param2=value)
- Extract query parameters from the URL and use them in the helper file
- Remove query parameters from the path statement
- Add them using `And params` statement

Example:
If endpoint is: `/api/users?includeDetails=true&page=1`
Then:
- path should be: `/api/users`
- params should be: `And params {{ includeDetails: '#(args.includeDetails)', page: '#(args.page)' }}`


- **Complex request building for nested objects:**
  - Build nested objects step-by-step using `set` command
  - Create empty objects first: `* def exportV3Request = {{}}`
  - Set properties individually: `* set exportV3Request.pageNumber = '#(args.pageNumber)'`
  - Handle conditional arrays and objects
- `Given headers tokenClass.returnAuthHeaders(args.tenant)` for authentication
- `Given path '[api-endpoint-path]'` as separate statement
- **Request handling rules:**
  - For complex requests, build requestPayload object using set commands
  - Use `And request requestPayload` for complex objects
  - If request payload is empty `{{}}`, DO NOT include `And request` line at all
  - For simple requests: Direct JSON object in request line
  - For complex requests: Build step-by-step using set commands
  - For lists: Use karate.append() to build arrays
- **Parameters handling:**
  - If query parameters are provided, use single line format: `And params {{ entityId: '#(args.entityId)',isConsolRedirected: '#(args.isConsolRedirected)' }}`
- `When method [HTTP_METHOD]`
- Examples table with at least 3 different test data combinations
- All parameters should be defined in defaultArgs with placeholder values like '<parameterName>'
- Never hardcode values - always use '#(args.parameterName)' to reference dynamic values
= Include ALL these parameters in defaultArgs: tenant, fileExportId, tenantId, transactionId, fileExportType, fileFormat, pageNumber, pageSize, sortField, sortDirection, priority, searchTerm, filterOperation, filterField, filterValue, filterValues, excelColumns, exportAllPages, decimalFormat, selectedIds, customExportRequest, fileName, entityType, entityId
- Use the exact structure shown in the example for building arrays and objects
- The filterCriteria should have a simple structure with operation, field, value, and values fields

### 2. Request Building Patterns:

#### Pattern A: Simple Direct Request
For simple flat JSON requests:
```
And request {{"field1": '#(args.field1)', "field2": '#(args.field2)'}}
```

#### Pattern B: Object Building with Arrays
For requests with objects that need to be in arrays:
```
# Build main object
* def mainObject = {{}}
* set mainObject.field1 = args.field1
* set mainObject.field2 = parseFloat(args.field2)

# Build array
* def objectList = []
* def objectList = karate.append(objectList, mainObject)

# Build request payload
* def requestPayload = {{}}
* set requestPayload.dataList = objectList

And request requestPayload
```

#### Pattern C: Complex Nested Structures
For deeply nested requests:
```
# Build nested components
* def nestedObject = {{}}
* set nestedObject.property1 = args.property1

# Build arrays conditionally
* def conditionalArray = []
* if (args.field != '') conditionalArray.push({{"item": '#(args.field)'}})

# Assemble final payload
* def requestPayload = {{}}
* set requestPayload.mainField = nestedObject
* set requestPayload.arrayField = conditionalArray
```

#### Pattern D: Query Parameters (No Body)
For GET requests with parameters:
```
And params {{ param1: '#(args.param1)', param2: '#(args.param2)' }}
```

#### Pattern E: Empty Request
For requests with no body:
```
# No "And request" line needed
```


### Complete Parameter Mapping Rules:

1. **Every parameter in defaultArgs MUST be used in the request**
   - Parameters should map to either:
   - Direct fields in the request body
   - Nested object properties
   - Array elements
   - Query parameters
   - Path parameters

2. **Dynamic Value Usage - STRICT RULES:**
 ```
NEVER hardcode values:
* set object.type = 'FIXED_TYPE'  // WRONG
* set object.flag = true           // WRONG

ALWAYS use args:
* set object.type = args.type      // CORRECT
* set object.flag = args.flag      // CORRECT
```

3. **Type Conversion Reference:**
   ```
- **Strings**: Use directly as `args.fieldName`
- **Numbers**: Use `parseInt(args.fieldName)` for integers
- **Decimals**: Use `parseFloat(args.fieldName)` for decimals
- **Booleans**: Use directly as `args.booleanField` (no parseBoolean needed) and add == 'true'
- **Arrays from strings**: Use `karate.fromString(args.arrayField)` for JSON arrays passed as strings
- **Objects**: Parse using appropriate method or build programmatically
   ```

4. **Conditional Parameter Usage:**
   ```
   * def sortParameters = []
   * if (args.sortField != '') sortParameters.push({{"sortField": args.sortField, "sortDirection": args.sortDirection, "priority": parseInt(args.priority)}})
   ```

5. **Complete Example Mapping:**
   If defaultArgs contains:
   ```
   {{tenant: '<tenant>', fileExportId: '<fileExportId>', tenantId: '<tenantId>', 
    transactionId: '<transactionId>', fileExportType: '<fileExportType>', 
    fileFormat: '<fileFormat>', pageNumber: '<pageNumber>', pageSize: '<pageSize>', 
    sortField: '<sortField>', sortDirection: '<sortDirection>', priority: '<priority>'}}
   ```

   Then ALL these parameters MUST appear in the request:
   ```
   * set requestPayload.fileExportId = '#(args.fileExportId)'
   * set requestPayload.tenantId = '#(args.tenantId)'
   * set requestPayload.transactionId = '#(args.transactionId)'
   * set requestPayload.fileExportType = '#(args.fileExportType)'
   * set requestPayload.fileFormat = '#(args.fileFormat)'
   * set exportV3Request.pageNumber = parseInt(args.pageNumber)
   * set exportV3Request.pageSize = parseInt(args.pageSize)
   * if (args.sortField != '') sortParameters.push({{"sortField": '#(args.sortField)', "sortDirection": '#(args.sortDirection)', "priority": parseInt(args.priority)}})
   ```

6. **Validation Checklist:**
   - Every parameter in defaultArgs is used somewhere
   - No hardcoded values (everything comes from args)
   - Proper type conversion applied (parseInt, parseFloat, parseBoolean)
   - Conditional logic for optional parameters
   - Nested objects built step-by-step

### 2. Main File Must Include:
- `Feature: [API Name] API Main Test Suite`
- Background section: `* def helper = read('[helper-filename].feature')`
- At least 7 different Scenario Outline sections covering various test scenarios
- Response validation: `* match result.response != null` and `* assert result.responseStatus == 200`
- Comprehensive Examples tables with varied test data (minimum 3-6 examples per scenario)
- Helper calls using * def result = call read('helper@[tagName]') {{[parameters]}}
- Response validation: * match result.response != null and * assert result.responseStatus == 200

### 3. Test Case Categories to Include:
- Basic valid data combinations
- Different data format variations
- Edge cases with valid data
- Multiple tenant testing
- Boundary value testing
- Field-specific variations (different formats, lengths, etc.)
- Multi-environment testing
- Empty and null value testing
- Complex nested object variations

### 4. Data Types Handling:
- **Strings**: Plain text without quotes (e.g., `tenant1`, `USD`, `value123`)
- **Numbers**: No quotes (e.g., `100`, `10.5`, `0`)
- **Booleans**: Lowercase without quotes (e.g., `true`, `false`)
- **Empty values**: Nothing between pipes (e.g., `|  |`)
- **JSON Arrays**: As strings (e.g., `["item1","item2"]`, `[]`)
- **JSON Objects**: As strings (e.g., `{{"key":"value"}}`, `{{}}`)
- **For object array values: [{{"id":"1"}},{{"id":"2"}}]
- **For empty/null value: leave empty or use {{}}
- **For string array values: ["VALUE1","VALUE2"]
- **For object array values: [{{"id":"1"}},{{"id":"2"}}]
- **For empty array values: []
- **karate.fromString() usage**: This function properly converts JSON string representations to actual objects/arrays.
- **Conditional building**: Filter criteria is only added when filterOperation is provided.
- **Empty object/array handling**: Explicit handling of empty objects `{{}}` and empty arrays `[]`.
- **Type flexibility**: The value field can now handle strings, numbers, booleans, objects, or remain empty.


### 5. Naming Conventions:
- Helper file: `[apiname]-helper.feature`
- Main file: `[apiname]-main.feature`
- Tag name: `@[apiActionName]`
- Scenario names: Descriptive and specific

### 10. Background Section Options:
```
# Option 1: Standard imports
Background: Define URL
  Given url customsURL
  * def utils = Java.type('utils.CommonUtils')
  * def tokenClass = Java.type('helper.UserHelper')

# Option 2: Additional utilities
Background:
  * def tokenClass = Java.type('helper.UserHelper')
  * def fetchArgs = function(mandatoryFields, defaultArgs) {{ return defaultArgs }}
  * def dateUtils = Java.type('utils.DateUtils')
```

## Analysis Guidelines:

When analyzing the provided API:
  - **Identify Request Pattern**: Determine if it's simple, complex, nested, or array-based
  - **Extract All Parameters**: List every field that should be parameterized
  - **Determine Data Types**: Identify strings, numbers, booleans, arrays, objects
  - **Check for Conditionals**: Note optional fields or conditional logic
  - **Consider Business Logic**: Understand relationships between fields



### 6. Complex Request Building:
For APIs with nested objects and arrays, build the request step-by-step:
- Create empty objects and arrays first
- Use conditional logic for optional fields
- Build nested structures using set commands
- Combine all parts into final requestPayload

### 7. Conditional Logic in Helper Files:
- Use Karate's conditional syntax: `* if (condition) action`
- For optional fields that depend on input:
  ```
  * if (args.sortField != '') sortParameters.push({{"sortField": args.sortField, sortDirection": args.sortDirection}})
  ```
- Build arrays conditionally based on input presence
- Handle empty arrays and objects gracefully

## Template Structure

### Simple Helper File Template:
```
@[tagName]
Feature: [API Name] API Helper

Scenario Outline: [API Action] API Helper
  * def mandatoryFields = ['tenant', 'field1', 'field2', 'field3']
  * def defaultArgs = {{tenant: '<tenant>', field1: '<field1>', field2: '<field2>', field3: '<field3>'}}
  * def args = fetchArgs(mandatoryFields, defaultArgs)
  Given headers tokenClass.returnAuthHeaders(args.tenant)
  Given path '[api-endpoint-path]'
  And request {{"field1": '#(args.field1)', "field2": '#(args.field2)', "field3": '#(args.field3)'}}
  When method [HTTP_METHOD]
  Examples:
    | tenant    | field1    | field2 | field3  |
    | tenant1   | value1    | 123    | value3  |
```
### Generic Complex Helper File Template:
```
@[tagName]
Feature: [API Name] API Helper
  Background: Define URL
    * def utils = Java.type('utils.CommonUtils')
    * def tokenClass = Java.type('helper.UserHelper')

  Scenario Outline: [API Action] API Helper
    * def mandatoryFields = ['tenant'[ADDITIONAL_FIELDS]]
    * def defaultArgs = {{tenant: '<tenant>'[ADDITIONAL_DEFAULT_ARGS]}}
    * def args = fetchArgs(mandatoryFields, defaultArgs)

    # Build main object with all fields
    * def [OBJECT_NAME] = {{}}
    [FIELD_ASSIGNMENTS]

    # Build array containing the object
    * def [OBJECT_LIST_NAME] = []
    * def [OBJECT_LIST_NAME] = karate.append([OBJECT_LIST_NAME], [OBJECT_NAME])

    # Build final request payload
    * def requestPayload = {{}}
    * set requestPayload.[LIST_PROPERTY_NAME] = [OBJECT_LIST_NAME]

    Given headers tokenClass.returnAuthHeaders(args.tenant)
    Given path '[API_ENDPOINT_PATH]'
    And request requestPayload
    When method [HTTP_METHOD]

    Examples:
      | tenant[EXAMPLE_HEADERS] |
      | [EXAMPLE_DATA_ROWS] |

### Template Placeholders Guide:

[ADDITIONAL_FIELDS]: Add all field names as strings
Example: , 'requestId', 'amount', 'currency', 'description'

[ADDITIONAL_DEFAULT_ARGS]: Add all default arg mappings
Example: , requestId: '<requestId>', amount: '<amount>', currency: '<currency>', description: '<description>'

[OBJECT_NAME]: Name for the main object being built
Example: chargeRequest, orderRequest, paymentRequest

[FIELD_ASSIGNMENTS]: Add set statements for each field with appropriate type conversion
Example:
    * set [OBJECT_NAME].requestId = args.requestId
    * set [OBJECT_NAME].amount = parseFloat(args.amount)
    * set [OBJECT_NAME].currency = args.currency
    * set [OBJECT_NAME].description = args.description
    * set [OBJECT_NAME].quantity = parseInt(args.quantity)
    * set [OBJECT_NAME].isActive = args.isActive
    * set [OBJECT_NAME].items = karate.fromString(args.items)

[OBJECT_LIST_NAME]: Name for the array containing objects
Example: chargeRequestList, orderRequestList, paymentRequestList

[LIST_PROPERTY_NAME]: Property name in final payload
Example: chargeRequests, orders, payments

[API_ENDPOINT_PATH]: Full URL or relative path
Example: /api/v1/charges/bulk-create
Example: https://api.domain.com/v1/orders/bulk

[HTTP_METHOD]: HTTP method
Example: POST, PUT, DELETE

[TAG_NAME]: Descriptive tag name in camelCase
Example: bulkChargeCreate, orderBulkUpdate, paymentProcess

[EXAMPLE_HEADERS]: Column headers for test data
Example: | requestId | amount | currency | description | quantity | isActive | items |

[EXAMPLE_DATA_ROWS]: Test data rows
Example: 
      | WFMUser | REQ001 | 100.50 | USD | Test charge    | 5  | true  | ["item1","item2"] |
      | tenant2 | REQ002 | 200.00 | EUR | Another charge | 10 | false | []                |
      | tenant3 | REQ003 | 0.0    | GBP | Empty charge   | 0  | true  | ["single"]        |

### Type Conversion Patterns:

For String fields:
    * set [OBJECT_NAME].fieldName = args.fieldName

For Float/Decimal fields:
    * set [OBJECT_NAME].fieldName = parseFloat(args.fieldName)

For Integer fields:
    * set [OBJECT_NAME].fieldName = parseInt(args.fieldName)

For Boolean fields:
    * set [OBJECT_NAME].fieldName = args.fieldName == 'true'

For Array fields (from JSON string):
    * set [OBJECT_NAME].fieldName = karate.fromString(args.fieldName)

For Optional fields (with condition):
    * if (args.fieldName != '') set [OBJECT_NAME].fieldName = args.fieldName
```
### Complete Example Usage:
```
@[tagName]
Feature: [API Name] API Helper
  Background: Define URL
    * def utils = Java.type('utils.CommonUtils')
    * def tokenClass = Java.type('helper.UserHelper')

  Scenario Outline: Invoice Charge Bulk Create API Helper
    * def mandatoryFields = ['tenant', 'chargeId', 'amount', 'currency', 'taxRate', 'items']
    * def defaultArgs = {{tenant: '<tenant>', chargeId: '<chargeId>', amount: '<amount>', currency: '<currency>', taxRate: '<taxRate>', items: '<items>'}}
    * def args = fetchArgs(mandatoryFields, defaultArgs)

    # Build main object with all fields
    * def chargeRequest = {{}}
    * set chargeRequest.chargeId = args.chargeId
    * set chargeRequest.amount = parseFloat(args.amount)
    * set chargeRequest.currency = args.currency
    * set chargeRequest.taxRate = parseFloat(args.taxRate)
    * set chargeRequest.items = karate.fromString(args.items)

    # Build array containing the object
    * def chargeRequestList = []
    * def chargeRequestList = karate.append(chargeRequestList, chargeRequest)

    # Build final request payload
    * def requestPayload = {{}}
    * set requestPayload.charges = chargeRequestList

    Given headers tokenClass.returnAuthHeaders(args.tenant)
    Given path '/api/endpoint'
    And request requestPayload
    When method POST

    Examples:
      | tenant  | chargeId | amount | currency | taxRate | items            |
      | WFMUser | CHG001   | 100.50 | USD      | 10.0    | ["item1"]        |
      | tenant2 | CHG002   | 200.00 | EUR      | 20.0    | ["item1","item2"]|
      | tenant3 | CHG003   | 0.0    | GBP      | 0.0     | []               |

```
### Helper File Template (with parameters):
```
@[tagName]
Feature: [API Name] API Helper

Scenario Outline: [API Action] API Helper
  * def mandatoryFields = ['tenant', 'entityId', 'isConsolRedirected']
  * def defaultArgs = {{tenant: '<tenant>', entityId: '<entityId>', isConsolRedirected: '<isConsolRedirected>'}}
  * def args = fetchArgs(mandatoryFields, defaultArgs)
  Given headers tokenClass.returnAuthHeaders(args.tenant)
  Given path '[api-endpoint-path-without-query-params]'  # Remove ?entityId=value&isConsolRedirected=true from here
  And params {{ entityId: '#(args.entityId)',isConsolRedirected: '#(args.isConsolRedirected)' }}
  When method [HTTP_METHOD]
  Examples:
    | tenant    | entityId  | isConsolRedirected |
    | tenant1   | entity1   | true               |
```

### Helper File Template (empty request):
```
@[tagName]
Feature: [API Name] API Helper

Scenario Outline: [API Action] API Helper
  * def mandatoryFields = ['tenant']
  * def defaultArgs = {{tenant: '<tenant>'}}
  * def args = fetchArgs(mandatoryFields, defaultArgs)
  Given headers tokenClass.returnAuthHeaders(args.tenant)
  Given path '[api-endpoint-path]'
  When method [HTTP_METHOD]
  Examples:
    | tenant    |
    | tenant1   |
```

### Main File Template:
```
Feature: [API Name] API Main Test Suite

Background:
  * def helper = read('[helper-filename].feature')

Scenario Outline: [Test Scenario Description]
  * def result = call read('helper@[tagName]') {{ tenant: '<tenant>',field1: '<field1>',field2: '<field2>',field3: '<field3>'}}
  * match result.response != null
  * assert result.responseStatus == 200
  Examples:
    | tenant | field1  | field2 | field3  |
    | tenant | value1  | 123    | value3  |
```

## Input Required from User:
Please provide the following information:
1. **API endpoint path** (e.g., '/consumer/file-export/process-file-export-request')
2. **HTTP method** (GET, POST, PUT, DELETE)
3. **Request payload structure** including:
   - Top-level fields and their data types
   - Nested objects and their properties
   - Array fields and their structure
   - Optional vs required fields
4. **Query parameters** (if any) with field names and data types
5. **Complex data types**:
   - JSON objects in string format (e.g., {{"value":"PAID"}})
   - Arrays of values (e.g., [{{"value":"INV"}},{{"value":"CRD"}}])
   - Nested structures
6. **Business logic**:
   - Which fields are conditional (only included when not empty)
   - When to include/exclude certain fields
   - Default values for optional fields
7. **API purpose/description** (e.g., "Process File Export Request")

## Examples Table Guidelines:
- Include comprehensive test data covering all scenarios
- Use empty strings '' for optional fields
- Use proper JSON format for complex objects: `{{"key":"value"}}`
- Include arrays in proper format: `[{{"id":"1"}},{{"id":"2"}}]`
- Minimum 3 rows of varied test data
- Cover edge cases like empty values, maximum lengths, special characters
- For complex nested data, ensure variety in nested fields


## Critical Rules:
- **FIRST CHECK**: Does the endpoint URL contain query parameters (look for '?')?
- **IF URL HAS QUERY PARAMS**: Extract them and use "Helper File Template (with parameters)"

- **NEVER** use multi-line JSON strings for simple request payload
- **For complex requests**, use step-by-step building with set commands
- **IF request payload is empty {{}}**, DO NOT include `And request` line at all
- **IF query parameters exist**, use single line format: `And params {{ param1: '#(args.param1)',param2: '#(args.param2)' }}`
- **ALWAYS** include 'tenant' in mandatoryFields
- **ALWAYS** use angle brackets in defaultArgs: `{{tenant: '<tenant>'}}`
- **ALWAYS** create at least 7 different scenario outlines in main file
- **ALWAYS** include comprehensive test data covering various scenarios
- NEVER use quotes ('') or double quotes ("") around simple values in Examples table
- Use proper JSON format for complex objects in Examples table
- Helper file should come first, followed by main file
- **NEVER** use code blocks (```gherkin or ```) in output
- **NEVER** use any markdown formatting in output
- **ALWAYS** return raw feature file content without any formatting
- **ABSOLUTELY NO CODE BLOCKS OR MARKDOWN FORMATTING**
- For complex nested requests, ALWAYS use set commands to build the request step by step
- Include Background section with Java imports for complex helpers
- **NEVER** use code blocks or markdown formatting
- **ALWAYS** parameterize all values (no hardcoding)
- **ALWAYS** include tenant in mandatory fields
- **ALWAYS** use proper type conversions
- **MATCH** the request structure to the API's actual needs
- **BUILD** complex objects step by step when needed
- **USE** karate.append() for building arrays
- **PLACE** @tagName before Examples section
- **CREATE** at least 7 meaningful test scenarios
- **PROVIDE** realistic and varied test data

## Expected Output:
Generate two complete feature files following the exact format shown above, with comprehensive test coverage and proper Karate syntax. Helper file should come first, followed by main file.

**Output Format:**

******************* Helper File ***************
[helper file content here]

******************* Main File ***************
[main file content here]

IMPORTANT: DO NOT USE ```gherkin OR ANY CODE BLOCKS IN THE OUTPUT

""")