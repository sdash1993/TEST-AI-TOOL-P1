from langchain_core.prompts import PromptTemplate

rest_api_prompt = PromptTemplate.from_template(
    """
API End point :-  {endpoint}

Method :- {method_type}

Request Payload :- {payload}
# Universal REST Assured API Automation Generator

## Instructions for LLM:

You are an expert REST Assured automation framework generator. Based on the API specification provided through template variables, generate a complete REST Assured automation framework with the following components:


### Required Components to Generate:

1. **POJO Classes** - With Lombok annotations (@Data, @Builder, @NoArgsConstructor, @AllArgsConstructor)
2. **API Helper Class** - With methods for the specific API endpoint
3. **Data Provider Class** - With TestNG data providers for different test scenarios
4. **Test Class** - With comprehensive test methods
5. **Utility Classes** - For validation and common operations
6. **Configuration Class** - For environment and base URL management
7. DONOT REPLY WITH ANY TEXT OTHER THAN THE REQUIRED FILES
8. DONOT REPLY WITH I UNDERSTAND
9. DONOT SUPPLY EXPLAINATION IN THE REPLY
10.DONOT USE ```java or ``` CODE BLOCKS

### Generation Rules:

#### For POJO Classes:
- Use Lombok annotations: `@Data`, `@Builder`, `@NoArgsConstructor`, `@AllArgsConstructor`
- Use `@JsonProperty` for field mapping
- Handle nested objects as separate POJO classes
- Use appropriate Java types (String, Integer, Boolean, List<String>, etc.)
- Generate builder pattern support
- Analyze the {{payload}} structure to create appropriate POJOs
- If {{additionalFilterRequest}} is provided, create a separate POJO for it

#### For Helper Class:
- Create method specific to {{method_type}} (GET, POST, PUT, DELETE, PATCH)
- Handle query parameters dynamically
- Handle request body for POST/PUT/PATCH methods
- Include authentication support using {{token}}
- Add {{tenantId}} as header if provided
- Add logging for requests and responses
- Create overloaded methods for different parameter combinations
- Use {{endpoint}} as the API endpoint

#### For Data Provider:
- Create multiple data providers for positive and negative scenarios
- Include boundary value testing data
- Handle different combinations of query parameters
- Generate realistic test data based on the {{payload}} structure
- Use {{id}} for resource identification in test data
- Include {{additionalFilterRequest}} in test scenarios

#### For Test Class:
- Use TestNG framework
- Include assertions for status code, response time, content type
- Add validation for response structure
- Include both positive and negative test cases
- Use data providers for parameterized testing
- Name test class as {{name}}APITest

#### For Additional Classes:
- Create validation utility class with common assertion methods
- Add configuration class for environment management
- Include error handling and logging
- Use {{name}} in class naming conventions

### Code Quality Requirements:
- Follow Java naming conventions
- Add comprehensive comments
- Include proper exception handling
- Use meaningful variable names based on {{name}}
- Ensure code is production-ready
- Replace template variables with actual values

### Response Format:
Provide complete, compilable Java code with proper package structure. Replace all template variables with actual values from the provided specification.

---

## Code Generation Template:

### 1. Main Request POJO Class:
```java
package com.api.pojos;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class {{name}}Request {{
  // Generate fields based on {{payload}} structure
  // Parse JSON and create appropriate fields with @JsonProperty
  // Example structure based on payload analysis
}}
```

### 2. API Helper Class:
```java
package com.api.helpers;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;
import java.util.Map;

public class {{name}}APIHelper {{

  private static final String ENDPOINT = "{{endpoint}}";
  private static final String AUTH_TOKEN = "{{token}}";
  private static final String TENANT_ID = "{{tenantId}}";

  public static RequestSpecification getRequestSpec() {{
      RequestSpecification spec = RestAssured.given()
              .contentType(ContentType.JSON)
              .accept(ContentType.JSON)
              .log().all();

      // Add authentication if token provided
      if (AUTH_TOKEN != null && !AUTH_TOKEN.isEmpty()) {{
          spec.header("Authorization", "Bearer " + AUTH_TOKEN);
      }}

      // Add tenant ID if provided
      if (TENANT_ID != null && !TENANT_ID.isEmpty()) {{
          spec.header("X-Tenant-ID", TENANT_ID);
      }}

      return spec;
  }}

  // Generate method based on {{method_type}}
  public static Response execute{{name}}Request({{name}}Request request, Map<String, Object> queryParams) {{
      RequestSpecification spec = getRequestSpec();

      if (queryParams != null && !queryParams.isEmpty()) {{
          spec.queryParams(queryParams);
      }}

      // Handle different HTTP methods
      if ("{{method_type}}".equalsIgnoreCase("GET")) {{
          return spec.when().get(ENDPOINT).then().log().all().extract().response();
      }} else if ("{{method_type}}".equalsIgnoreCase("POST")) {{
          return spec.body(request).when().post(ENDPOINT).then().log().all().extract().response();
      }} else if ("{{method_type}}".equalsIgnoreCase("PUT")) {{
          return spec.body(request).when().put(ENDPOINT).then().log().all().extract().response();
      }} else if ("{{method_type}}".equalsIgnoreCase("DELETE")) {{
          return spec.when().delete(ENDPOINT).then().log().all().extract().response();
      }}

      return spec.body(request).when().post(ENDPOINT).then().log().all().extract().response();
  }}
}}
```

### 3. Data Provider Class:
```java
package com.api.dataproviders;

import com.api.pojos.{{name}}Request;
import org.testng.annotations.DataProvider;
import java.util.HashMap;
import java.util.Map;

public class {{name}}DataProvider {{

  @DataProvider(name = "valid{{name}}Data")
  public Object[][] valid{{name}}Data() {{
      return new Object[][] {{
          {{
              createValidRequest(),
              createValidQueryParams()
          }}
      }};
  }}

  @DataProvider(name = "invalid{{name}}Data")
  public Object[][] invalid{{name}}Data() {{
      return new Object[][] {{
          {{
              createInvalidRequest(),
              createInvalidQueryParams()
          }}
      }};
  }}

  private static {{name}}Request createValidRequest() {{
      // Build valid request based on {{payload}} structure
      return {{name}}Request.builder()
              // Add fields based on payload analysis
              .build();
  }}

  private static {{name}}Request createInvalidRequest() {{
      // Build invalid request for negative testing
      return {{name}}Request.builder()
              // Add invalid data for testing
              .build();
  }}

  private static Map<String, Object> createValidQueryParams() {{
      Map<String, Object> params = new HashMap<>();
      params.put("page", 1);
      params.put("size", 10);
      // Add more based on API requirements
      return params;
  }}

  private static Map<String, Object> createInvalidQueryParams() {{
      Map<String, Object> params = new HashMap<>();
      params.put("page", -1);
      params.put("size", 0);
      return params;
  }}
}}
```

### 4. Test Class:
```java
package com.api.tests;

import com.api.dataproviders.{{name}}DataProvider;
import com.api.helpers.{{name}}APIHelper;
import com.api.pojos.{{name}}Request;
import io.restassured.response.Response;
import org.testng.Assert;
import org.testng.annotations.Test;
import java.util.Map;

public class {{name}}APITest {{

  @Test(dataProvider = "valid{{name}}Data", dataProviderClass = {{name}}DataProvider.class)
  public void test{{name}}ValidRequest({{name}}Request request, Map<String, Object> queryParams) {{
      Response response = {{name}}APIHelper.execute{{name}}Request(request, queryParams);

      // Validate status code based on method type
      if ("{{method_type}}".equalsIgnoreCase("POST")) {{
          Assert.assertTrue(response.getStatusCode() == 200 || response.getStatusCode() == 201,
                  "POST request should return 200 or 201");
      }} else if ("{{method_type}}".equalsIgnoreCase("GET")) {{
          Assert.assertEquals(response.getStatusCode(), 200, "GET request should return 200");
      }}

      Assert.assertNotNull(response.getBody(), "Response body should not be null");
      Assert.assertTrue(response.getTime() < 5000, "Response time should be less than 5 seconds");
  }}

  @Test(dataProvider = "invalid{{name}}Data", dataProviderClass = {{name}}DataProvider.class)
  public void test{{name}}InvalidRequest({{name}}Request request, Map<String, Object> queryParams) {{
      Response response = {{name}}APIHelper.execute{{name}}Request(request, queryParams);

      Assert.assertTrue(response.getStatusCode() >= 400, "Should return error status code");
  }}

  @Test
  public void test{{name}}Unauthorized() {{
      // Test without authentication
      {{name}}Request request = {{name}}Request.builder().build();
      Response response = {{name}}APIHelper.execute{{name}}Request(request, null);

      // May return 401 or 403 depending on API implementation
      Assert.assertTrue(response.getStatusCode() == 401 || response.getStatusCode() == 403,
              "Should return unauthorized status");
  }}
}}
```

### 5. Configuration Class:
```java
package com.api.config;

import lombok.Data;

@Data
public class APIConfig {{
  public static final String BASE_URL = System.getProperty("base.url", "https://api.example.com");
  public static final String AUTH_TOKEN = System.getProperty("auth.token", "{{token}}");
  public static final String TENANT_ID = System.getProperty("tenant.id", "{{tenantId}}");
  public static final String ENVIRONMENT = System.getProperty("environment", "dev");

  public static String getBaseUrl() {{
      switch (ENVIRONMENT.toLowerCase()) {{
          case "prod": return "https://prod-api.com";
          case "staging": return "https://staging-api.com";
          case "dev": 
          default: return "https://dev-api.com";
      }}
  }}
}}
```

### 6. Validation Utility:
```java
package com.api.utils;

import io.restassured.response.Response;
import org.testng.Assert;

public class ValidationUtils {{

  public static void validateStatusCode(Response response, int expectedCode) {{
      Assert.assertEquals(response.getStatusCode(), expectedCode, 
                        "Expected status: " + expectedCode + ", Actual: " + response.getStatusCode());
  }}

  public static void validateResponseTime(Response response, long maxTime) {{
      Assert.assertTrue(response.getTime() <= maxTime, 
                       "Response time exceeded: " + response.getTime() + "ms");
  }}

  public static void validateFieldExists(Response response, String fieldPath) {{
      Assert.assertNotNull(response.jsonPath().get(fieldPath), 
                         "Field should exist: " + fieldPath);
  }}

  public static void validateContentType(Response response, String expectedType) {{
      Assert.assertTrue(response.getContentType().contains(expectedType),
                       "Content type should contain: " + expectedType);
  }}
}}
```

---

## Maven Dependencies:
```xml
<dependencies>
  <!-- REST Assured -->
  <dependency>
      <groupId>io.rest-assured</groupId>
      <artifactId>rest-assured</artifactId>
      <version>5.3.0</version>
  </dependency>

  <!-- TestNG -->
  <dependency>
      <groupId>org.testng</groupId>
      <artifactId>testng</artifactId>
      <version>7.8.0</version>
  </dependency>

  <!-- Jackson -->
  <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-databind</artifactId>
      <version>2.15.2</version>
  </dependency>

  <!-- Lombok -->
  <dependency>
      <groupId>org.projectlombok</groupId>
      <artifactId>lombok</artifactId>
      <version>1.18.28</version>
      <scope>provided</scope>
  </dependency>

  <!-- JSON Path -->
  <dependency>
      <groupId>io.rest-assured</groupId>
      <artifactId>json-path</artifactId>
      <version>5.3.0</version>
  </dependency>
</dependencies>
```

---

## Additional Instructions:

1. **Parse the {{payload}} JSON** to automatically generate POJO fields
2. **Use {{name}}** as the prefix for all class names
3. **Handle {{method_type}}** appropriately in helper methods
4. **Include {{token}}** in authentication headers
5. **Add {{tenantId}}** as custom header if provided
6. **Use {{id}}** for resource identification in tests
7. **Incorporate {{additionalFilterRequest}}** in data providers
8. **Generate realistic test data** based on the actual payload structure
9. **Create both positive and negative test scenarios**
10. **Include proper error handling and logging**

**Output Format:**
generate the complete REST Assured automation framework using the provided template variables, with comprehensive test coverage and proper syntax.

******************* POJO Classes ***************
[POJO Classes content here]
******************* API Helper Class ***************
[API Helper Classes content here]
******************* Data Provider Class ***************
[Data Provide content here]
******************* Utility Classes ***************
[Utility Classes content here]
******************* Configuration Class ***************
[Configuration Class content here]
******************* Test Class ***************
[Test Class content here]


IMPORTANT: DO NOT USE ```java OR ANY CODE BLOCKS IN THE OUTPUT


""")