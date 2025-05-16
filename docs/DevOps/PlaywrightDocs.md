#  🚀 Exciting Milestone: Mastering Playwright Automation Testing! 🚀

![Playwright](https://github.com/sawanchouksey/documents/blob/main/docs/DevOps/Playwright.png?raw=true)

🎓 **Learning Journey:**
What an exciting and insightful experience it's been! From understanding the fundamentals of Playwright to exploring its advanced features, I’ve gained a deeper appreciation for its capabilities. I’ve had the opportunity to work with:

* **Multiple Browser Automation:** Testing across Chrome, Firefox, and WebKit with just one script!
* **Headless Testing:** Efficiently running tests in a headless browser environment.
* **Parallel Testing:** Dramatically reducing testing time and increasing efficiency.
* **Robust Debugging Tools:** Utilizing powerful tools like Playwright Inspector to track down issues with precision.
* **API Testing:** Integrating API and UI testing for end-to-end automation.

🔧 **Key Benefits of Using Playwright:**

1. **Cross-browser Testing:** Automate testing on multiple browsers seamlessly. Playwright supports Chrome, Firefox, and Safari (WebKit) with a single framework.

2. **Speed and Efficiency:** With its ability to run tests in parallel and headless mode, Playwright drastically reduces test execution time and boosts productivity.

3. **Rich API Support:** It’s perfect for testing web applications from different angles – UI, API, and performance testing.

4. **Stable and Reliable:** Playwright’s API is robust, offering accurate automation results and minimizing flaky tests.

5. **Easy Setup & Configuration:** Setting up Playwright is intuitive, and its powerful debugging tools make identifying issues faster than ever.

## Fake data generator 
https://www.npmjs.com/package/@faker-js/faker

## Playwright dockert images 
- `version of docker images` must be match with playwright `version in package.json` 
```
mcri.microsoft.com/playwright:v1.37.0-jammy
```

## Github Action with Playwright
- Playwright `CI` with `github action`
```yaml
name: Playwright Tests
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: 20
    - name: Install dependencies
      run: npm ci --force
    - name: Install Playwright Browsers
      run: npx playwright install --with-deps --force
    - name: Run Playwright tests
      run: npm run pageObjects-chrome
    - uses: actions/upload-artifact@v4
      if: ${{ !cancelled() }}
      with:
        name: playwright-report
        path: playwright-report/
        retention-days: 30
```

- **Playwright Test Dockerfile**
```Dockerfile
FROM mcr.microsoft.com/playwright:v1.37.1-jammy

RUN mkdir /app
WORKDIR /app
COPY . /app/

RUN npm install --force
RUN npx playwright install
```

- **Playwright Test docker-compose.yaml**
```yaml
version: '3.8'
services:
  playwright-test:
    image: playwright-test
    build:
      context: .
      dockerfile: ./Dockerfile
    command: npm run pageObjects-chrome
    volumes:
      - ./playwright-report/:/app/playwright-report
      - ./test-results/:/app/test-results
```

## Demo Web Application
```
cd NodeJsApplication4WebTesting
npm install --force
npm install webpack
npm start
http://localhost:4200/
```
## TypeScript 
- Variable Defination
```typescript
let user: {name:string, age:number} = {name: "bob", age: 34};
```
## Playwright Command 

- Runs the end-to-end tests.
```
npx playwright test
```

- Starts the interactive UI mode.
```
npx playwright test --ui
```

- Runs the tests only on Desktop Chrome.
```
npx playwright test --project=chromium
```

- Runs the tests in a specific file.
```
npx playwright test example
```

- Runs the tests in debug mode.
```
npx playwright test --debug
```

- Auto generate tests with Codegen.
```
npx playwright codegen
```

- We suggest that you begin by typing:
```
npx playwright test
```

- And check out the following files:
    - .\tests\example.spec.ts - Example end-to-end test
    - .\tests-examples\demo-todo-app.spec.ts - Demo Todo App end-to-end tests
    - .\playwright.config.ts - Playwright Test configuration

- Run a single test file instead of all
```
npx playwright test <folderNameContainsTestCasesFiles>/<fileNameContainTestCase.spec.ts>
npx playwright test tests/example.spec.ts
```

- check generated report
```
npx playwright show-report
```

## `Playwright` configuration files settings and available option
- `playwright` configuration file for command
```
npx playwright test tests/lcient.spect.js --config playwright.config1.js
```

- `specific configuration` based on project execution with **playwright.config.js**
```javascript
projects : [
    {
      name : 'safari',
      use: {

        browserName : 'webkit',
        headless : true,
        screenshot : 'off',
        trace : 'on',//off,on 
        ...devices['iPhone 11'],    
      }

    },
    {
      name : 'chrome',
      use: {

        browserName : 'chromium',
        headless : false,
        screenshot : 'on',
        video: 'retain-on-failure',
        ignoreHttpsErrors:true,
        permissions:['geolocation'],
        
        trace : 'on',//off,on
       // ...devices['']
     //   viewport : {width:720,height:720}
         }

    }
    ]

npx playwright test tests/client.spect.js --project safari
```

- to run playwright test for specific `devices`
```javascript
projects : [
    {
      name : 'safari',
      use: {

        browserName : 'webkit',
        headless : true,
        screenshot : 'off',
        trace : 'on',//off,on 
        ...devices['iPhone 11'],    
      }
    },
]
```

- for ignore `ssl` error page to click **advanced** for move to website page due to untrusted Https certificate
```javascript
projects : [
    {
      name : 'safari',
      use: {

        browserName : 'webkit',
        headless : true,
        screenshot : 'off',
        ignoreHttpsErrors: true,
        trace : 'on',//off,on 
        ...devices['iPhone 11'],    
      }

    },
```

- permission set on `browser` for playwright automation
```javascript
projects : [
    {
      name : 'safari',
      use: {

        browserName : 'webkit',
        headless : true,
        screenshot : 'off',
        permission: ['geolocation'],
        trace : 'on',//off,on 
        ...devices['iPhone 11'],    
      }
    },
```

- `Record video` option in 
   - 'off' - Do not record video.
   - 'on' - Record video for each test.
   - 'retain-on-failure' - Record video for each test, but remove all videos from successful test runs.
   - 'on-first-retry' - Record video only when retrying a test for the first time.

```javascript
import { defineConfig } from '@playwright/test';
export default defineConfig({
  use: {
    video: 'on-first-retry',
  },
});
```

- to fix `flaky tests(didn't passed in first attempt but successfull only multiple retries count)` with test `retry option` in playwright config file

```javascript
retries: 10
```

- playwright run tests in `serial & parallel` mode and update setting
   - We can control parallel mode by `worker` setting to execution counts each file is equal to 1.
   - by default `playwright` runs at `worker = 5` only
```javascript
// It will execute 2 test files at a time
workers: 2; 
```

- run `tests parallely` from the same file by `extending test option` behaviour
```javascript
// it will to run run 3 test from same file in 3 workers. Bydefault it runs on 'serial` mode only 
test.describe.configure({mode: 'parallel'})
```

- How to `tag tests` and `control the execution` from the command line parameters
```javascript
test('@tagName ClientApp login for ${data.productName}', async ({page}) )=>{
   ....
}

// It will execute all test available in all files with same tag.
npx playwright test --grep @tagName
```
## How to generate `HTML & Allure` reporting for Playwright Framework tests
- first install the **allure-playwright** node modules 
   - **line** reporting used for generate report in `text format`
```
npm i -D @playwright/test allure-playwright

npx playwright test --grep @Web --reporter=line,allure-playwright

#use to generate allure reports from allure results
allure generate ./allure-result --clean

#use to open allure report
allure open ./allure-results
```

## create `custom scripts` to trigger the tests from package.json file
```json
"scripts": {
   "regression": "npx playwright test",
   "webTest": "npx playwright test --grep @tagName",
   "APItest": "npx playwright test --grep @tagName --reporter=line,allure-playwright"
}

# Execute test with below command using `npm`
npm run webTest
```

## Integrate `Playwright` with `jenkins`

- Run jenkins by `jenkins.war`
```cmd
java -jar jenkins.war -httpPort=9090
http://localhost:9090
```
- configure `job`
- configure `git` url for `automation playwright script` src code
- add `build step`
   - invoke `batch command` 
   ```cmd
   npm run webtest
   ```
   - or `shell command`
   ```shell
   npm run webtest
   ```
- click `build Now` button

##  Introduction to `Azure DevOps & Playwright cloud workspace` resource creation steps

- Create `Microsoft Playwright testing` in Azure portal

`Azure Portal`-->`Marketplace`-->`Search: Playwright`-->`Select: Microsoft Playwright Testing`-->`Create`-->

- Create a `Workspace` in azure portal
![Microsoft Playwright](https://playwright.microsoft.com)

- Install `Microsoft Playwright Testing` package in src Code and add dependency in **package.json**
```
npm init @azure/microsoft-playwright-testing
```

- add the following in **playwright.config.js**
```javascript
export default defineConfig(
   config,
   getServiceConfig(config, {
      exposeNetwork: '<loopback>',
      timeout: 30000
      os: ServiceOS.LINUX,
      // set to false if you want to only use reporting
      useCloudHostedBrowsers: true 
   }),
   {
      reporter: [['list'], ['@azure/microsoft-playwright-testing/reporter']],
   } 
) 
```

- Configure `Azure` 
```
az login
export PLAYWRIGHT_SERVICE_URL=wss://westeurope.api.playwright.microsoft.com/accounts/westeurpoe_udeuiay897/browsers
```

- finally run your test
```
npx playwright test --config=playwright.service.config.ts --workers=20
```

- AzureCI/CD `Pipelines.yml` file
```yml
jobs:
  - job: Build
    steps:
      - task: PowerShell@2
        enabled: true
        displayName: "Install dependencies"
        inputs:
          targetType: 'inline'
          script: 'npm ci'
          workingDirectory: tests/ # update accordingly
 
      - task: AzureCLI@2
        displayName: Run Playwright Test
        env:
          PLAYWRIGHT_SERVICE_URL: $(PLAYWRIGHT_SERVICE_URL)
          PLAYWRIGHT_SERVICE_RUN_ID: $(Build.DefinitionName) - $(Build.BuildNumber) - $(System.JobAttempt)
        inputs:
          azureSubscription: 'rahulshettyacademy' # Service connection used to authenticate this pipeline with Azure to use the service
          scriptType: 'pscore'
          scriptLocation: 'inlineScript'
          inlineScript: |
            npx playwright test  --config=playwright.service.config.js           
          addSpnToEnvironment: true
          
 
      - task: PublishPipelineArtifact@1
        displayName: Upload Playwright report
        inputs:
          targetPath: tests/playwright-report/ # update accordingly
          artifact: 'Playwright tests'
          publishLocation: 'pipeline'
```

## Selectors rules for automation TS

1. **If Id is present:**
   ```typescript
   // CSS selector using tag name and ID
   const element = await page.$('tagname#id');
   // CSS selector using only ID
   const element = await page.$('#id');
   ```

2. **If class attribute is present:**
   ```typescript
   // CSS selector using tag name and class
   const element = await page.$('tagname.class');
   // CSS selector using only class
   const element = await page.$('.class');
   ```

3. **Write CSS based on any attribute:**
   ```typescript
   // CSS selector using attribute and value
   const element = await page.$('tagname[attribute="value"]');
   ```

4. **Write CSS with traversing from parent to child:**
   ```typescript
   // CSS selector for parent to child traversal
   const element = await page.$('parenttagname > childtagname');
   ```

5. **If needs to write the locator based on text:**
   ```typescript
   // CSS selector based on text content
   const element = await page.$('tagname:contains("text")');
   ```

6. **Selecting elements by attribute presence:**
   ```typescript
   // Select elements with a specific attribute
   const elements = await page.$$('tagname[attribute]');
   ```

7. **Selecting elements by partial attribute value:**
   ```typescript
   // Select elements where the attribute contains a specific value
   const elements = await page.$$('tagname[attribute*="value"]');
   ```

8. **Selecting elements by attribute starting value:**
   ```typescript
   // Select elements where the attribute starts with a specific value
   const elements = await page.$$('tagname[attribute^="value"]');
   ```

9. **Selecting elements by attribute ending value:**
   ```typescript
   // Select elements where the attribute ends with a specific value
   const elements = await page.$$('tagname[attribute$="value"]');
   ```

10. **Selecting elements by nth-child:**
   ```typescript
   // Select the nth child element
   const element = await page.$$('tagname:nth-child(n)');
   ```

11. **Selecting elements by pseudo-class:**
   ```typescript
   // Select elements with a specific pseudo-class
   const elements = await page.$$('tagname:pseudo-class');
   ```

12. **Combining multiple selectors:**
   ```typescript
   // Combine multiple selectors to narrow down the selection
   const elements = await page.$$('tagname.class[attribute="value"]:pseudo-class');
   ```

13. **XPATH Selector**
   - Any Selector starting with `//` or `..` are assumed to be an xpath selector. 
   ```typescript
   // using Xpath selector
   await page.locator('//html/body').click();
   // Playwright converts '//html/body' to 'xpath=//html/body'
   ```

## Timeouts in Playwright Automation

1. **Global Timeout**
   - **Default:** No timeout
   - **Description:** This is the time limit for the entire test run.
   - **Example:** If you set a global timeout of 60,000 ms (1 minute), the entire test suite must complete within this time frame.

2. **Test Timeout**
   - **Default:** 30,000 ms (30 seconds)
   - **Description:** This is the time limit for a single test.
   - **Example:** If a test takes longer than 30 seconds, it will fail due to a timeout.

3. **Action Timeout**
   - **Default:** No timeout
   - **Description:** This is the time limit for individual action commands like `click()`, `fill()`, `textContent()`, etc.
   - **Example:** `await page.click('button#submit', { timeout: 5000 });` - This sets a 5-second timeout for the click action.

4. **Navigation Timeout**
   - **Default:** No timeout
   - **Description:** This is the time limit for navigation commands like `page.goto()`.
   - **Example:** `await page.goto('https://example.com', { timeout: 10000 });` - This sets a 10-second timeout for the navigation.

5. **Expect Timeout**
   - **Default:** 5000 ms (5 seconds)
   - **Description:** This is the time limit for "expect" locator assertions.
   - **Example:** `await expect(locator).toHaveText('Hello World', { timeout: 3000 });` - This sets a 3-second timeout for the assertion.

### Short Example and Explanation

```javascript
const { test, expect } = require('@playwright/test');

test('example test with timeouts', async ({ page }) => {
  // Set global timeout for the test
  test.setTimeout(60000); // 1 minute

  // Navigate to the page with a navigation timeout
  await page.goto('https://example.com', { timeout: 10000 }); // 10 seconds

  // Perform an action with an action timeout
  await page.click('button#submit', { timeout: 5000 }); // 5 seconds

  // Expect an element to have specific text with an expect timeout
  await expect(page.locator('h1')).toHaveText('Welcome', { timeout: 3000 }); // 3 seconds
});
```

**Explanation:**
- The global timeout is set to 1 minute for the entire test.
- The navigation to `https://example.com` must complete within 10 seconds.
- The click action on the submit button must complete within 5 seconds.
- The assertion that the `h1` element contains the text "Welcome" must complete within 3 seconds.


## Playwright Automation Code Syntax

- `await` is used for **Action Items** performance only.
    - **Action perfomed `inside` locator bracket only**
    ```javascript
    console.log(await page.locator(".classNameRadioButton").last().isChecked());
    ```

    - **Action perfomed `outside` locator bracket only**
    ```javascript
    expect(await page.locator('#terms').isChecked()).toBeFalsy();
    ```

- Use `locator()` to find css element and selector for page to traverse through action by script.
```javascript
await page.locator('#username').fill("sawan");
```

- `Resusing the locator` in scripts
```typescript
const basicForm = page.locator('nb-card').filter({hasText: "Basic Form"})
const emailField = basicForm.getByRole('textbox',{name: "Email"})

await basicForm.getByRole('textbox',{name: "Email"}).fill('test@test.com')
await basicForm.getByRole('textbox',{name: "Password"}).fill('wel@1234')
await basicForm.getByRole('button').click()

await expect(emailField).toHaveValue('test@test.com')
```

- Use `fill()` instead of `type()` to enter something in **textboxes**. Because `type` is depreceted and even you will using it. it will strike.
```javascript
await page.locator("[type='password']").fill("sawan45678");
```

- use `click()` to click on button.
```javascript
await page.locator("#signInButton").click();
```

- to extract the `text message` from the `alert` in page where text is visible for sometime due to css **style=`display: none;`** and print in console
```javascript
\\webdriverWait
console.log(await page.locator("[stype*='block']")).textContent();
```

- put `assertion` using **expect** to decide whether `test is passed or failed` and here we check `text` inside the locator
```
await expect(page.locator("[stype*='block']")).toContainText('Incorrectfet`);
```

- define `variable` in js and use it
```javascript

//defining
const userName = page.locator('#username');
//using variable
await userName.fill("Sawan");
```

- Clear the content from the `textbox`
```javascript
await userName.fill("");
```

- `traversing` from **Parent** to **child** css selector 
```
.parentsclass child tag|Attribute
.card-body a 
```

- find tiltle of `first element` from multiple element from `css selector` using array and print in console
```javascript
// method 1
console.log(await page.locator(".card-body a").nth(0).textContent());
// method 2
console.log(await page.locator(".card-body a").first().textContent());
```

- find the titles of `all element` from multiple element from `css selector` and get result in `array` format
```javascript
const allTitles = await page.locator(".card-body a").allTextContents();
console.log(allTitles);
```

- wait for complete all network call to completely load the page
```javascript
await page.waitForLoadState('networkidle');
```

- wait for the load specific `css element` in web page also the `first & last occurence` only.
```javascript
await page.waitForLoadState(".card-body b").waitFor();
await page.waitForLoadState(".card-body b").first().waitFor();
await page.waitForLoadState(".card-body b").last().waitFor();
```

- static drop-down use `select` tag and select values
```javascript
const dropdown = page.locator("select.form-control");
awaits dropdown.selectOption("doctor");
// pause page to see result also know as playwright inspector for debug and troubleshoot
await page.pause();
```

- select `radio` button option with CSS class Name `classNameRadioButton` and alert option css id name `idokaybutton` and check `radio` button to test passed 
```javascript
await page.locator(".classNameRadioButton").last().click();
await page.locator("#idokaybtn").click(); 
// to checked checkboc is correctly set or not return true or false instead of failing test case
console.log(await page.locator(".classNameRadioButton").last().isChecked());
await expect(page.locator(".classNameRadioButton").last()).toBeChecked();
```

- check and uncheck `checkbox` after selecting it once
```javascript
//check the checkbox
await page.locator("#termsConditions").click();
//uncheck the checkbox
await page.locator("#termsConditions").uncheck();
```

- failed the `testcase` if checkbox is **not uncheck** means it must return `false for uncheck` and `true for check`
```javascript
expect(await page.locator('#terms').isChecked).toBeFalsy();
```

- check if the `link` is blinking or not in web page or some css attribute i.e. **class BlinkingText** exist or not
```javascript
const documentLink = page.locator("[href*='document-request']");
await expect(documentLink).toHaveAttribute("class", "BlickingText");
```

- Works with `child windows` or `new page` landing when open in new tab
```Javascript
test('@child Windows hadl', async({browser})=>
    const context = await browser.newContext();
    const page = await context.newPage();
    // load all child windows operation inside `promiseall` within exisiting page
    // It returns page in array format even you can call multiple page as well.
    const [newPage,newPage1..newPage..n] = await Promise.all([
        //listen for new page and wait for current events as complete pending,fullfilled or rejected
        context.waitForEvent('page'),
        // click on the link,button to load the child window or page in parent page
        documentLink.click(),
    ]) // new Page is opened

    text = await newPage.locator(".red").textContent();
    console.log(text);
    // extract hightlight 'emailID' from the text
    // split the text based on `@' symbol
    const arrayText = text.split("@")
    const domain = arrayText[1].split(" ")[0]
    console.log(domain)
    // fill value from extracted child window
    await page.locator("#username").type(domain);
    // pause the playwright execution for watch performing action in web page
    await page.pause()
    console.log(await page.locator("#username").textContent());
)
```

- Enable `screenshot` for each step action executed and enable `trace` as well
```javascript
\\playwright.config.ts
use: {
    browserName: 'chromium',
    screenshot: 'on',
    trace: 'on',
}
```

- to get multiple items and select using for loops
```javascript
const productName = "Adidas Shoes"
const products = page.locator(".card-body");
const count = await products.count();
for(let i=0; i<count; ++i)
{
   // looking css attribute `b` within `card-body` only not in whole web page css attribute within loop
   if(await products.nth(i).locator("b").textContent() === productName)
   {
      // use css attribute having text `add to card` to add product in cart
      await products.nth(i).locator("text = Add to Cart").click();
      // break after successfull finding the element
      break;
   }
}
// to use another atrribute to 'reach cart page'
// locator("[routerLink*='cart']"): The locator method is used to find elements on the page. The argument "[routerLink*='cart']" is a CSS selector that targets elements with a routerLink attribute containing the substring 'cart'. The *= operator is used for partial matching.
//await: This keyword is used to wait for the promise to resolve. In this case, it waits for the click action to complete before moving on to the next line of code. It's typically used in asynchronous functions.
await page.locator("[routerLink*='cart']").click();

//isVisible method does not automatically wait for the element to appear, so you need to use an alternative approach to ensure the element is present before checking its visibility.
//Wait for the first li element inside a div to appear. 
await page.locator("div li").first().waitFor();
//locator("div li"): Finds all li elements inside div elements.
//.first(): Selects the first li element from the list of matched elements.
//.waitFor(): Waits for the first li element to appear in the DOM.

//Check if an h3 element containing the text 'Adidas Shoes' is visible
const bool = page.locator("h3:has-text('Adidas Shoes')").isVisible();
//const bool: Declares a constant variable bool.
//page.locator("h3:has-text('Adidas Shoes')"): Finds an h3 element that contains the text 'Adidas Shoes'.
//.isVisible(): Checks if the located h3 element is visible on the page and returns a boolean value.

//Assert that the element is visible
expect(bool).toBeTruthy();
//expect(bool): Uses the expect function to create an assertion for the bool variable.
//.toBeTruthy(): Asserts that the bool variable is true, meaning the element is visible.
```

- This code types "ind" into an input field, waits for a dropdown to appear, counts the number of options, loops through them to find the option with the text "India", clicks it, and then pauses the script.
```javascript
// Type 'ind' into an input field with a placeholder containing 'Country'
await page.locator("[placeholder*='Country']").type("ind",{delay:100});
//page.locator("[placeholder*='Country']"): Finds an input field with a placeholder attribute containing the substring 'Country'.
//.type("ind", { delay: 100 }): Types the string "ind" into the input field with a delay of 100 milliseconds between each keystroke.

// Locate the dropdown element
const dropdown = page.locator(".ta-results");
//const dropdown: Declares a constant variable dropdown.
//page.locator(".ta-results"): Finds an element with the class ta-results.

// Wait for the dropdown to appear
await dropdown.waitFor()

// Count the number of button elements in the dropdown
const optionCount = await dropdown.locator("button").count();

// Loop through each button element in the dropdown
for (let i=0; i < optionCount ; i++)
{
   // Get the text content of each button element
   const text = await dropdown.locator("button").nth(i).textContent();

   //Check if the text content is 'India' and click the button if it is
   if (text === "India")
   {
      await dropdown.locator("button").nth(i).click();
      break;
   }
   //if (text === "India"): Checks if the text content is 'India'.
   //await dropdown.locator("button").nth(i).click(): Clicks the i-th button element if the text content is 'India'.
   //break: Exits the loop once the button is clicked.
}

//Pause the script execution
await page.pause();
//await: Waits for the promise to resolve.
//page.pause(): Pauses the script execution, allowing you to inspect the browser state.
```

- fetch Specific element from the web page containing table and click on it i.e. get `order id` from `MyOrders` table and click on `view` button to order details
```javascript
// Click the 'myorders' button
await page.locator("button[routerlink*='myorders']").click();
//page.locator("button[routerlink*='myorders']"): Finds a button element with a routerlink attribute containing the substring 'myorders'.

// Wait for the tbody element to appear means table body
await page.locator("tbody").waitFor();

// Locate all rows within the tbody
const rows = await page.locator("tbody tr");
// page.locator("tbody tr"): Finds all tr elements within the tbody

// Loop through each row to find the matching order ID
for (let i = 0; i < await rows.count(); ++i) {
   const rowOrderId = await rows.nth(i).locator("th").textContent();
   if (orderId.includes(rowOrderId)) {
      await rows.nth(i).locator("button").first().click();
      break;
   }
}
// for (let i = 0; i < await rows.count(); ++i): A for loop that iterates from 0 to the number of rows minus one.
// await rows.nth(i).locator("th").textContent(): Retrieves the text content of the th element in the i-th row.
// if (orderId.includes(rowOrderId)): Checks if the orderId variable contains the rowOrderId.
// await rows.nth(i).locator("button").first().click(): Clicks the first button in the i-th row if the orderId matches

//Get the text content of the order ID details
const text = await dropdown.locator("button").nth(i).textContent();
//dropdown.locator("button").nth(i): Selects the i-th button element within the dropdown.
//.textContent(): Retrieves the text content of the selected button element.

// Check if the text content is 'India' and click the button if it is
if (text === "India") {
   await dropdown.locator("button").nth(i).click();
   break;
}
// await dropdown.locator("button").nth(i).click(): Clicks the i-th button element if the text content is 'India
const orderIdDetails = await page.locator(".col-text").textContent();
expect(orderId.includes(orderIdDetails)).toBeTruthy();
await page.pause();
```

- Work with Playwright `inBuitMethod`  getByLabel(),getByText() etc.
   
   -  **Import Statements** 
      ```javascript
      test('Playwright Special locators', async ({ page }) => {
      ```
      - **test**: Defines a test case named 'Playwright Special locators'.
      - **async ({ page }) =>**: An asynchronous function that provides a `page` object to interact with the browser.

   - **Navigating to a URL**
      ```javascript
      await page.goto("https://rahulshettyacademy.com/angularpractice/");
      ```
      - **page.goto**: Navigates to the specified URL.

   - **Interacting with Elements**
      ```javascript
      await page.getByLabel("Check me out if you Love IceCreams!").click();
      ```
      - **page.getByLabel**: Finds an element by its label text.
      - **click**: Clicks on the found element.

      ```javascript
      await page.getByLabel("Employed").check();
      ```
      - **check**: Checks a checkbox or radio button.

      ```javascript
      await page.getByLabel("Gender").selectOption("Female");
      ```
      - **selectOption**: Selects an option from a dropdown menu.

      ```javascript
      await page.getByPlaceholder("Password").fill("abc123");
      ```
      - **getByPlaceholder**: Finds an element by its placeholder text.
      - **fill**: Fills the found element with the specified text.

      ```javascript
      await page.getByRole("button", {name: 'Submit'}).click();
      ```
      - **getByRole**: Finds an element by its role (e.g., button, link).
      - **click**: Clicks on the found element.

   - **Verifying Conditions**
      ```javascript
      await page.getByText("Success! The Form has been submitted successfully!.").isVisible();
      ```
      - **getByText**: Finds an element by its text content.
      - **isVisible**: Checks if the found element is visible on the page.

   - **Navigating and Interacting with More Elements**
      ```javascript
      await page.getByRole("link",{name : "Shop"}).click();
      ```
      - **getByRole**: Finds a link element by its role and name.
      - **click**: Clicks on the found element.

      ```javascript
      await page.locator("app-card").filter({hasText: 'Nokia Edge'}).getByRole("button").click();
      ```
      - **locator**: Finds elements matching the specified CSS selector.
      - **filter**: Filters elements based on their text content.
      - **getByRole**: Finds a button element within the filtered elements.
      - **click**: Clicks on the found button.

- End to end example of **validating calendars** with assertion in playwright

   - **Import Statements**
      ```javascript
      const { test, expect } = require("@playwright/test");
      ```
      - **require**: Imports the `test` and `expect` functions from the Playwright testing library.

   - **Test Definition**
      ```javascript
      test("Calendar validations", async ({ page }) => {
      ```
      - **test**: Defines a test case named "Calendar validations".
      - **async ({ page }) =>**: An asynchronous function that provides a `page` object to interact with the browser.

   - **Variable Declarations**
      ```javascript
      const monthNumber = "6";
      const date = "15";
      const year = "2027";
      const expectedList = [monthNumber, date, year];
      ```
      - **const**: Declares constants for the month, date, and year to be selected.
      - **expectedList**: An array containing the expected values for the selected date.

   - **Navigating to a URL**
      ```javascript
      await page.goto("https://rahulshettyacademy.com/seleniumPractise/#/offers");
      ```
      - **page.goto**: Navigates to the specified URL.

   - **Interacting with the Calendar Date Picker**
      ```javascript
      await page.locator(".react-date-picker__inputGroup").click();
      ```
      - **locator**: Finds an element matching the specified CSS selector.
      - **click**: Clicks on the found element.

      ```javascript
      await page.locator(".react-calendar__navigation__label").click();
      await page.locator(".react-calendar__navigation__label").click();
      ```
      - **click**: Clicks on the calendar navigation label twice to open the year selection view.

      ```javascript
      await page.getByText(year).click();
      ```
      - **getByText**: Finds an element by its text content (the year) and clicks on it.

      ```javascript
      await page.locator(".react-calendar__year-view__months__month").nth(Number(monthNumber) - 1).click();
      ```
      - **nth**: Selects the nth element in a list (zero-based index). Here, it selects the month based on the `monthNumber`.

      ```javascript
      await page.locator("//abbr[text()='" + date + "']").click();
      ```
      - **locator**: Uses an XPath selector to find the date element and clicks on it.

   - **Verifying the Selected Date**
      ```javascript
      const inputs = await page.locator(".react-date-picker__inputGroup input");
      for (let index = 0; index < inputs.length; index++) {
         const value = inputs[index].getAttribute("value");
         expect(value).toEqual(expectedList[index]);
      }
      ```
      - **locator**: Finds all input elements within the date picker input group.
      - **for loop**: Iterates over each input element.
      - **getAttribute**: Retrieves the value attribute of each input element.
      - **expect**: Asserts that the value of each input matches the expected value from `expectedList`.

- Handline `Visible|Hide` element and `Alert` Popup in browser
```javascript
await expect (page.locator('#Displayed-text')).toBeVisible();
await page.locator('#hide-textbox').click()
await expect (page.locator('#Displayed-text')).toBeHidden();
await page.pause();

//dialog.accept() = ok or accept && dialog.dissmiss() = cancel or reject at alert popup message
page.on('dialog', dialog => dialog.accept());
await page.locator('#confirmbtn').click();

// hover on the specific item
await page.locator('#mousehover').hover();
```

- working with `iframe` frames in web pages
```javascript
const framepage = page.frameLocator("#courses-iframe");
// Selects the iframe with the ID 'courses-iframe' and assigns it to 'framepage'.

await framepage.locator("li a[href*='lifetime-accesss']:visible").click();
// Waits for and clicks the visible link containing 'lifetime-accesss' within the iframe.

const textcheck = await framepage.locator(".txtt h2").textContent();
// Retrieves the text content of the <h2> element within the class 'txtt' in the iframe.

console.log(textcheck.split(" ")[1]);
// Logs the second word of the retrieved text content to the console.
```
## Playwright Inspector and Debugging playwright script
- To run `playwright script` in debugging mode and it will open playwright `inspector` in web browser
```
npx test tests/code.spec.js --debug
```

- 
```javascript
class APiUtils {
    constructor(apiContext, loginPayLoad) {
        this.apiContext = apiContext; // Store the API context for making requests
        this.loginPayLoad = loginPayLoad; // Store the login payload for authentication
    }
 
    async getToken() {
        // Make a POST request to the login endpoint with the login payload
        const loginResponse = await this.apiContext.post("https://rahulshettyacademy.com/api/ecom/auth/login", {
            data: this.loginPayLoad // Send the login payload as the request body
        }); // Expecting a 200 or 201 response status
        const loginResponseJson = await loginResponse.json(); // Parse the response JSON
        const token = loginResponseJson.token; // Extract the token from the response
        console.log(token); // Log the token to the console
        return token; // Return the token
    }
 
    async createOrder(orderPayLoad) {
        let response = {};
        response.token = await this.getToken(); // Get the authentication token
        // Make a POST request to the create order endpoint with the order payload
        const orderResponse = await this.apiContext.post("https://rahulshettyacademy.com/api/ecom/order/create-order", {
            data: orderPayLoad, // Send the order payload as the request body
            headers: {
                'Authorization': response.token, // Include the token in the Authorization header
                'Content-Type': 'application/json' // Set the content type to JSON
            }
        });
 
        const orderResponseJson = await orderResponse.json(); // Parse the response JSON
        console.log(orderResponseJson); // Log the response JSON to the console
        const orderId = orderResponseJson.orders[0]; // Extract the order ID from the response
        response.orderId = orderId; // Store the order ID in the response object
 
        return response; // Return the response object containing the token and order ID
    }
}
module.exports = { APiUtils }; // Export the APiUtils class for use in other modules
```

- `apiIntegration()` with playwright in webPages GUI testing
   - `test.beforeEach()` and `test.afterEach()` hooks run **before/after each test** declared in the same file and same test.describe() block (if any). 
   - `test.beforeAll()` and `test.afterAll()` hooks run **before/after all tests** declared in the same file and same test.describe() block (if any), once per worker process. 
   - `addInitScript()`Adds a script which would be evaluated in one of the following scenarios:
      - Whenever the page is navigated.
      - Whenever the child frame is attached or navigated. In this case, the script is evaluated in the context of the newly attached frame.
   The script is evaluated after the document was created but before any of its scripts were run. 

```javascript
const {test, expect, request} = require('@playwright/test'); // Import necessary modules from Playwright
const {APiUtils} = require('../utils/APiUtils'); // Import the APiUtils class from the utils directory
const loginPayLoad = {userEmail:"anshika@gmail.com",userPassword:"Iamking@000"}; // Define the login payload with user credentials
const orderPayLoad = {orders:[{country:"Cuba",productOrderedId:"67a8dde5c0d3e6622a297cc8"}]}; // Define the order payload with order details
 
let response; // Initialize a variable to store the response
test.beforeAll( async() => {
   const apiContext = await request.newContext(); // Create a new API context for making requests
   const apiUtils = new APiUtils(apiContext, loginPayLoad); // Instantiate APiUtils with the API context and login payload
   response = await apiUtils.createOrder(orderPayLoad); // Create an order and store the response
});
 
// Test to place the order successfully
test('@API Place the order', async ({page}) => { 
    page.addInitScript(value => {
        window.localStorage.setItem('token', value); // Set the token in local storage
    }, response.token); // Pass the token from the response
    await page.goto("https://rahulshettyacademy.com/client"); // Navigate to the client page
    await page.locator("button[routerlink*='myorders']").click(); // Click on the 'My Orders' button
    await page.locator("tbody").waitFor(); // Wait for the orders table to load
    const rows = await page.locator("tbody tr"); // Get all rows in the orders table
 
    // Loop through the rows to find the order ID
    for(let i = 0; i < await rows.count(); ++i) {
        const rowOrderId = await rows.nth(i).locator("th").textContent(); // Get the order ID from the row
        if (response.orderId.includes(rowOrderId)) {
            await rows.nth(i).locator("button").first().click(); // Click the button in the row if the order ID matches
            break;
        }
    }
    const orderIdDetails = await page.locator(".col-text").textContent(); // Get the order details text
    // await page.pause(); // Uncomment to pause the test for debugging
    expect(response.orderId.includes(orderIdDetails)).toBeTruthy(); // Verify the order ID is in the details
});
 
// Verify if the created order is showing in the history page
// Precondition - create order
```
- pass data with `.json` file inside script **storage in session, cookies** etc.
```json
{
  "cookies": [],
  "origins": [
    {
      "origin": "https://rahulshettyacademy.com",
      "localStorage": [
        {
          "name": "token",
          "value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2Mjc0MjU0OWUyNmI3ZTFhMTBlOWZjZTAiLCJ1c2VyRW1haWwiOiJyYWh1bHNoZXR0eUBnbWFpbC5jb20iLCJ1c2VyTW9iaWxlIjo5NTQzNjQ1NzU0LCJ1c2VyUm9sZSI6ImN1c3RvbWVyIiwiaWF0IjoxNjk2NTQzNDM2LCJleHAiOjE3MjgxMDEwMzZ9.qz0D0OYg1A_6yxeoGPH-OTVl3MMfEVNuo1p7gEhxzjQ"
        }
      ]
    }
  ]
}
```

```javascript
//create global variable

let webContext
webContext = await context.storageState({path: 'state.json'});
await browser.netContext({storageState: 'state.json'});
```

- `Session storage` & `Intercepting Network request/responses` with Playwright `Route` method

```javascript
const { test, expect, request } = require('@playwright/test'); // Import necessary modules from Playwright
const { APiUtils } = require('../utils/APiUtils'); // Import the APiUtils class from the utils directory
const loginPayLoad = { userEmail: "anshika@gmail.com", userPassword: "Iamking@000" }; // Define the login payload with user credentials
const orderPayLoad = { orders: [{ country: "India", productOrderedId: "67a8dde5c0d3e6622a297cc8" }] }; // Define the order payload with order details
const fakePayLoadOrders = { data: [], message: "No Orders" }; // Define a fake payload to simulate no orders

let response; // Initialize a variable to store the response
test.beforeAll(async () => {
  const apiContext = await request.newContext(); // Create a new API context for making requests
  const apiUtils = new APiUtils(apiContext, loginPayLoad); // Instantiate APiUtils with the API context and login payload
  response = await apiUtils.createOrder(orderPayLoad); // Create an order and store the response
});
 
// Test to place the order successfully
test('@SP Place the order', async ({ page }) => {
  page.addInitScript(value => {
    window.localStorage.setItem('token', value); // Set the token in local storage
  }, response.token); // Pass the token from the response
  await page.goto("https://rahulshettyacademy.com/client"); // Navigate to the client page
 
  // Intercept the API request to get orders for the customer
  await page.route("https://rahulshettyacademy.com/api/ecom/order/get-orders-for-customer/*",
    async route => {
      const response = await page.request.fetch(route.request()); // Fetch the original request
      let body = JSON.stringify(fakePayLoadOrders); // Create a fake response body
      route.fulfill({
        response, // Use the original response
        body, // Replace the body with the fake response
      });
      // Intercepting response - API response -> { Playwright fake response } -> browser -> render data on front end
    });
 
  await page.locator("button[routerlink*='myorders']").click(); // Click on the 'My Orders' button
  await page.waitForResponse("https://rahulshettyacademy.com/api/ecom/order/get-orders-for-customer/*"); // Wait for the intercepted response
 
  console.log(await page.locator(".mt-4").textContent()); // Log the text content of the element with class 'mt-4'
});
```

- `Intercept Network request` calls with Playwright

```javascript
const { test, expect } = require('@playwright/test'); // Import necessary modules from Playwright

test('@QW Security test request intercept', async ({ page }) => {
 
    // Login and reach orders page
    await page.goto("https://rahulshettyacademy.com/client"); // Navigate to the client page
    await page.locator("#userEmail").fill("anshika@gmail.com"); // Fill in the email field
    await page.locator("#userPassword").fill("Iamking@000"); // Fill in the password field
    await page.locator("[value='Login']").click(); // Click the login button
    await page.waitForLoadState('networkidle'); // Wait for the network to be idle
    await page.locator(".card-body b").first().waitFor(); // Wait for the first product card to be visible
 
    await page.locator("button[routerlink*='myorders']").click(); // Click on the 'My Orders' button
    // Intercept the API request to get order details and modify the URL
    await page.route("https://rahulshettyacademy.com/api/ecom/order/get-orders-details?id=*",
        route => route.continue({ url: 'https://rahulshettyacademy.com/api/ecom/order/get-orders-details?id=621661f884b053f6765465b6' }));
    
    // intercepting response --> APi response -->{ Playwright fakeresponse}-->browser
    // get the response and store in variables
    const response = await page.request.fetch(route.request());
    let body = JSON.stringify(fakePayLoadOrders);
    route.fullfill(
      {
         response,
         body,
      }
   );  

    await page.pause();
    await page.locator("button:has-text('View')").first().click(); // Click the first 'View' button
    await expect(page.locator("p").last()).toHaveText("You are not authorize to view this order"); // Verify the unauthorized message
});

```

- `Block` all the network calls  and specific files from `Network calls`
```javascript
page.route('**/*.{jpg.png.jpeg}', route=> route.abort());
```

- record and fetch all `rquest & response` call in playwright test executed in browser
```javascript
page.on('request',request=>console.log(request.url()));
page.on('response',request=>console.log(response.url(), response.status()));
```

- take `screenshot` on element or locator level
```javascript
await page.locator("#display-text").screenshot({path: 'elemntlevelSS.png'});
```

- match `screenshot` with **playwrite automation** with browser i.e. visual testing
```javascript
test('visual'.async({page}))=>{
   await page.goto("https://www.rediff.com");
   expect(await page.screenshot()).toMatchSnapshot('landing.png');
})
```

- Use `Playwright` for automating browser interactions and `ExcelJs` for manipulating Excel files. It includes functions to `read and update Excel files, and a test case that downloads an Excel file`, updates a specific cell, and uploads the modified file back to a web application to verify the changes. The test also includes **intercepting network requests** to simulate different scenarios.

```javascript
const ExcelJs = require('exceljs'); // Import the ExcelJs library for working with Excel files
const { test, expect } = require('@playwright/test'); // Import necessary modules from Playwright
async function writeExcelTest(searchText, replaceText, change, filePath) {
  const workbook = new ExcelJs.Workbook(); // Create a new workbook instance
  await workbook.xlsx.readFile(filePath); // Read the Excel file from the specified file path
  const worksheet = workbook.getWorksheet('Sheet1'); // Get the worksheet named 'Sheet1'
  const output = await readExcel(worksheet, searchText); // Find the cell with the search text
  const cell = worksheet.getCell(output.row, output.column + change.colChange); // Get the cell to be updated
  cell.value = replaceText; // Set the new value for the cell
  await workbook.xlsx.writeFile(filePath); // Write the updated workbook back to the file
}

async function readExcel(worksheet, searchText) {
  let output = { row: -1, column: -1 }; // Initialize output object to store row and column of the search text
  worksheet.eachRow((row, rowNumber) => {
    row.eachCell((cell, colNumber) => {
      if (cell.value === searchText) { // Check if the cell value matches the search text
        output.row = rowNumber; // Store the row number
        output.column = colNumber; // Store the column number
      }
    });
  });
  return output; // Return the output object with row and column numbers
}

// Update Mango Price to 350
// writeExcelTest("Mango", 350, { rowChange: 0, colChange: 2 }, "/Users/rahulshetty/downloads/excelTest.xlsx");

test('Upload download excel validation', async ({ page }) => {
  const textSearch = 'Mango'; // Define the text to search in the Excel file
  const updateValue = '350'; // Define the value to update in the Excel file
  await page.goto("https://rahulshettyacademy.com/upload-download-test/index.html"); // Navigate to the test page
  const downloadPromise = page.waitForEvent('download'); // Wait for the download event
  await page.getByRole('button', { name: 'Download' }).click(); // Click the download button
  await downloadPromise; // Wait for the download to complete
  writeExcelTest(textSearch, updateValue, { rowChange: 0, colChange: 2 }, "/Users/rahulshetty/downloads/download.xlsx"); // Update the Excel file
  await page.locator("#fileinput").click(); // Click the file input element
  await page.locator("#fileinput").setInputFiles("/Users/rahulshetty/downloads/download.xlsx"); // Upload the updated Excel file
  const textlocator = page.getByText(textSearch); // Locate the text in the page
  const desiredRow = await page.getByRole('row').filter({ has: textlocator }); // Find the row containing the text
  await expect(desiredRow.locator("#cell-4-undefined")).toContainText(updateValue);
});  
```

- Page object method for `playwright` automation by *Class* mechanism

### **1. The `NavigationPage` Class (Page Object Pattern)**

```typescript
import { Page } from "@playwright/test"

export class NavigationPage {
   readonly page: Page

   constructor(page: Page) {
      this.page = page
   }

   async formLayout() {
      await this.page.getByText('Forms').click()
      await this.page.getByText('Form Layout').click()
   }
}
```

#### **Page Object Model (POM)**
This `NavigationPage` class is a **Page Object** used in automated testing with Playwright. The **Page Object Model** (POM) is a design pattern that allows us to abstract the UI interactions into a separate class. This provides several benefits, such as:

- **Reusability**: You can reuse the logic to navigate to a specific page without having to rewrite code.
- **Maintainability**: If the UI changes, you only need to update the page object instead of modifying every individual test.

#### **Class Description**
- `NavigationPage`: This is a class representing a specific page in the web application you are testing—in this case, the navigation page.
  
- **`readonly page: Page`**: The `NavigationPage` class has a property called `page`, which is an instance of the `Page` class from Playwright. This allows us to interact with the page in the browser.

- **Constructor (`constructor(page: Page)`)**: The constructor takes a `page` parameter, which is passed when the class is instantiated in the test. It initializes the `page` property, which is used in methods to perform actions on the page.

- **Method `formLayout()`**: This is an asynchronous method that simulates the navigation of the user. It performs the following steps:
  1. **`await this.page.getByText('Forms').click()`**: It clicks on an element with the text "Forms".
  2. **`await this.page.getByText('Form Layout').click()`**: After navigating to the "Forms" section, it clicks on an element with the text "Form Layout". This action mimics user behavior by clicking through the UI.

  The `await` keyword ensures that the script waits for each action to complete before moving on to the next one.

---

### **2. The Test File (Test Logic)**

```typescript
import { test, expect } from '@playwright/test'
import { NavigationPage } from '../page-objects/navigationPage'

test.beforeEach(async({ page }) => {
   await page.goto('http://localhost:4200/')
})

test('Navigation to form page', async({ page }) => {
   const navigateTo = new NavigationPage(page)
   await navigateTo.formLayout()
})
```

#### **Test Framework**
This file is where the actual test is written using **Playwright's test framework**. Playwright provides an easy way to write end-to-end tests using JavaScript or TypeScript. It interacts with the browser to simulate real user behavior and verify the behavior of the application.

#### **`test.beforeEach()`**:
- **Purpose**: This is a lifecycle hook in Playwright that runs before each individual test case.
- **Action**: Inside `beforeEach`, we have `await page.goto('http://localhost:4200/')`. This navigates the browser to the URL `http://localhost:4200/` (typically, this could be a local development server).
- **Why it’s important**: Every test needs to start from a clean state, and this setup ensures that the test starts on the desired page.

#### **Test Case (`test('Navigation to form page', async({ page }) => {...})`)**:
- **Purpose**: This is the actual test case where we define what we want to test.
  
- **Test Name**: `'Navigation to form page'` describes what the test is verifying. In this case, it checks that the navigation to the "Form Layout" page works as expected.
  
- **Test Steps**:
  1. **Create an instance of `NavigationPage`**: The test creates a new instance of the `NavigationPage` class, passing the `page` object (which Playwright automatically provides in the test context) to the constructor.
  2. **Call `formLayout()` method**: The `formLayout()` method is invoked on the `NavigationPage` instance. This simulates the user clicking through the navigation: first on "Forms" and then on "Form Layout".

#### **Assertions (Optional in this example)**:
- Although not included in this particular test case, you could use **expectations** like `expect()` in Playwright to verify that the page navigated correctly. For example:
  ```typescript
  await expect(page).toHaveURL('http://localhost:4200/form-layout')
  ```

### **Summary of How It Works Together**

- The `NavigationPage` class encapsulates the navigation logic and is reusable in different test scenarios.
- The `test.beforeEach` ensures the application is at the correct starting point before each test case.
- The actual test (`test('Navigation to form page')`) instantiates `NavigationPage`, and uses its methods to simulate user actions (clicking through the navigation).
  
### **Why This Structure Is Beneficial**

1. **Separation of Concerns**: The test focuses on verifying behavior, while the page object is responsible for handling interactions with the page.
2. **Reusability**: The `NavigationPage` class can be reused across multiple tests wherever navigation actions are required.
3. **Maintainability**: If the UI changes (e.g., if the text of the buttons changes), you only need to update the page object methods rather than updating every test that clicks those buttons.

## `Codegen` tool to record & playback with generated automation script
```
npx playwright codegen http://google.com
```

## **auto-waiting**
Playwright's auto-waiting features are designed to make your test scripts more reliable and less flaky by automatically waiting for certain conditions to be met before performing actions. Here are the key aspects of auto-waiting in Playwright:

### **Actionability Checks**

Playwright performs a range of actionability checks on elements before making actions to ensure these actions behave as expected. These checks include:

1. **Visibility**: Ensures the element is visible.
2. **Stability**: Ensures the element is stable and not animating.
3. **Receives Events**: Ensures the element is not obscured by other elements.
4. **Enabled**: Ensures the element is enabled and can be interacted with.

### **Examples of Auto-Waiting**

Here are some examples of how auto-waiting works with different actions:

1. **Clicking an Element**:
   ```typescript
   await page.click('selector');
   ```
   Playwright will wait for the element to be visible, stable, receive events, and be enabled before clicking.

2. **Filling an Input Field**:
   ```typescript
   await page.fill('selector', 'text');
   ```
   Playwright will wait for the input field to be visible, stable, and enabled before filling it with text.

3. **Pressing a Key**:
   ```typescript
   await page.press('selector', 'Enter');
   ```
   Playwright will wait for the element to be visible and focused before sending the keystroke.

### **Assertions with Auto-Retry**

Playwright also includes auto-retrying assertions that remove flakiness by waiting until the condition is met. For example:
   ```typescript
   await expect(page.locator('selector')).toBeVisible();
   ```
   This assertion will automatically retry until the element becomes visible.

### **Forcing Actions**

Some actions support a `force` option that disables non-essential actionability checks. For example:
   ```typescript
   await page.click('selector', { force: true });
   ```
   This will click the element without checking if it receives click events[1](https://playwright.dev/docs/actionability)[2](https://hicronsoftware.com/blog/playwright-auto-waits/).

### **Fixed Waits**

While auto-waiting is preferred, you can also use fixed waits if necessary:
   ```typescript
   await page.waitForTimeout(2000); // waits for 2 seconds
   ```



## References
- Visit https://playwright.dev/docs/intro for more information. ✨

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚
