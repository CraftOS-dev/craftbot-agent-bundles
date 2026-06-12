<!--
Source: https://maestro.dev/docs · https://wix.github.io/Detox/ · https://appium.io/ · https://webdriver.io/
Authored: June 2026 for the qa-engineer agent bundle.
-->

# Mobile Testing — Maestro + Detox + Appium + WebdriverIO

The 2026 mobile-E2E stack: **Maestro** (YAML, fastest setup, iOS / Android /
RN / Flutter / web) for greenfield; **Detox** (grey-box, < 2% flakiness)
for React Native; **Appium + WebdriverIO** (cross-platform / cross-language /
deepest ecosystem) for hybrid + multi-stack. Real-device cloud via BrowserStack
App Live / Sauce Real Device Cloud.

## When to use

- New mobile app needs E2E from day 1 (Maestro)
- React Native team needs the most stable mobile E2E (Detox)
- Mixed native + hybrid + web in same app (Appium / WDIO)
- Cross-platform team in Python / Java (Appium)
- Real-device coverage for top devices (BrowserStack / Sauce)
- Trigger phrases: "mobile E2E", "Maestro", "Detox", "Appium",
  "WebdriverIO", "iOS test", "Android test", "real device cloud"

## Setup

```bash
# Maestro
curl -Ls https://get.maestro.mobile.dev | bash
maestro --version

# Detox (React Native)
npm i -D detox @types/jest
brew tap wix/brew && brew install applesimutils    # iOS
npm i -g detox-cli

# Appium 2 + drivers
npm i -g appium
appium driver install uiautomator2    # Android
appium driver install xcuitest        # iOS
appium driver install flutter         # Flutter
appium driver install mac2            # macOS

# WebdriverIO + Appium
npm i -D @wdio/cli
npx wdio config
```

Auth: BrowserStack / Sauce credentials per recipes.

## Common recipes

### Recipe 1 — Maestro flow (YAML)

```yaml
# flows/login.yaml
appId: com.example.app
---
- launchApp
- tapOn: "Email"
- inputText: "alice@example.com"
- tapOn: "Password"
- inputText: "Test1234!"
- tapOn: "Sign In"
- assertVisible: "Dashboard"
- assertNotVisible: "Login"
```

```bash
maestro test flows/login.yaml
maestro test flows/ --include-tags="smoke" --format=junit > results.xml
maestro studio    # interactive recorder
```

### Recipe 2 — Maestro parameterized flows

```yaml
# flows/login_parametrized.yaml
appId: com.example.app
env:
  USERNAME: alice@example.com
  PASSWORD: Test1234!
---
- launchApp
- tapOn: "Email"
- inputText: ${USERNAME}
- tapOn: "Password"
- inputText: ${PASSWORD}
- tapOn: "Sign In"
- assertVisible: "Welcome"
```

```bash
maestro test flows/login_parametrized.yaml -e USERNAME=bob@example.com
```

### Recipe 3 — Maestro cloud (Mobile.dev cloud)

```bash
maestro cloud --apiKey $MAESTRO_API_KEY ./app-debug.apk flows/
# Returns CI-friendly report URL + JUnit
```

### Recipe 4 — Detox (React Native) test

```js
// e2e/login.test.js
describe("Login flow", () => {
  beforeAll(async () => {
    await device.launchApp({ delete: true });
  });

  it("logs in with valid credentials", async () => {
    await element(by.id("emailInput")).typeText("alice@example.com");
    await element(by.id("passwordInput")).typeText("Test1234!");
    await element(by.id("loginButton")).tap();
    await expect(element(by.id("dashboardTitle"))).toBeVisible();
  });

  it("shows error on invalid credentials", async () => {
    await element(by.id("emailInput")).clearText();
    await element(by.id("emailInput")).typeText("alice@example.com");
    await element(by.id("passwordInput")).typeText("wrong");
    await element(by.id("loginButton")).tap();
    await waitFor(element(by.text("Invalid credentials")))
      .toBeVisible().withTimeout(5000);
  });
});
```

```js
// .detoxrc.js
module.exports = {
  testRunner: { args: { config: "e2e/jest.config.js" } },
  apps: {
    "ios.debug": {
      type: "ios.app",
      binaryPath: "ios/build/Build/Products/Debug-iphonesimulator/MyApp.app",
      build: "xcodebuild ... -configuration Debug -sdk iphonesimulator -derivedDataPath ios/build",
    },
    "android.debug": {
      type: "android.apk",
      binaryPath: "android/app/build/outputs/apk/debug/app-debug.apk",
      build: "cd android && ./gradlew assembleDebug assembleAndroidTest -DtestBuildType=debug && cd ..",
    },
  },
  devices: {
    iphone15: { type: "ios.simulator", device: { type: "iPhone 15" } },
    pixel7: { type: "android.emulator", device: { avdName: "Pixel_7_API_34" } },
  },
  configurations: {
    "ios.sim.debug": { device: "iphone15", app: "ios.debug" },
    "android.emu.debug": { device: "pixel7", app: "android.debug" },
  },
};
```

```bash
detox build -c ios.sim.debug
detox test -c ios.sim.debug
detox test -c android.emu.debug --headless
```

### Recipe 5 — Appium + WebdriverIO config

```ts
// wdio.conf.ts
export const config = {
  runner: "local",
  port: 4723,
  specs: ["./test/specs/**/*.ts"],
  maxInstances: 1,
  capabilities: [
    {
      platformName: "iOS",
      "appium:deviceName": "iPhone 15",
      "appium:platformVersion": "17.5",
      "appium:automationName": "XCUITest",
      "appium:app": process.env.IOS_APP_PATH,
      "appium:newCommandTimeout": 240,
    },
    {
      platformName: "Android",
      "appium:deviceName": "Pixel_7_API_34",
      "appium:platformVersion": "14",
      "appium:automationName": "UiAutomator2",
      "appium:app": process.env.ANDROID_APK_PATH,
    },
  ],
  framework: "mocha",
  reporters: ["spec", ["junit", { outputDir: "./reports" }]],
};
```

```ts
// test/specs/login.test.ts
describe("Login", () => {
  it("logs in successfully", async () => {
    await $("~emailInput").setValue("alice@example.com");
    await $("~passwordInput").setValue("Test1234!");
    await $("~loginButton").click();
    await expect($("~dashboardTitle")).toBeDisplayed();
  });
});
```

```bash
appium &   # start server
npx wdio
```

### Recipe 6 — BrowserStack App Live (real device)

```yaml
# browserstack.yml
userName: ${BROWSERSTACK_USERNAME}
accessKey: ${BROWSERSTACK_ACCESS_KEY}
app: ./app-debug.apk
platforms:
  - deviceName: Samsung Galaxy S24
    osVersion: 14.0
    deviceOrientation: portrait
  - deviceName: iPhone 15 Pro
    osVersion: 17
parallelsPerPlatform: 1
```

```bash
npx browserstack-node-sdk wdio wdio.conf.ts
```

### Recipe 7 — Maestro CI run

```yaml
# .github/workflows/mobile.yml
on: [pull_request]
jobs:
  android-maestro:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: zulu, java-version: 17 }
      - name: AVD cache
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 34
          script: |
            curl -Ls https://get.maestro.mobile.dev | bash
            export PATH=$HOME/.maestro/bin:$PATH
            ./gradlew assembleDebug
            adb install -r app/build/outputs/apk/debug/app-debug.apk
            maestro test flows/ --format=junit > maestro-junit.xml
      - uses: actions/upload-artifact@v4
        if: always()
        with: { name: maestro-report, path: maestro-junit.xml }
```

### Recipe 8 — Detox CI run

```yaml
# .github/workflows/detox-ios.yml
on: [pull_request]
jobs:
  ios:
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: brew tap wix/brew && brew install applesimutils
      - run: npx detox build -c ios.sim.debug
      - run: npx detox test -c ios.sim.debug --record-logs all --headless
```

### Recipe 9 — Deep linking + push notifications

```yaml
# Maestro
- openLink: myapp://order/42
- assertVisible: "Order #42"
```

```js
// Detox
await device.openURL({ url: "myapp://order/42" });
await device.sendUserNotification({
  trigger: { type: "push" },
  payload: { aps: { alert: "New message" } },
});
```

### Recipe 10 — Screenshots + recording

```yaml
# Maestro
- takeScreenshot: "after-login"
- startRecording: "checkout-flow"
- ... actions ...
- stopRecording
```

```js
// Detox
await device.takeScreenshot("after-login");
await device.startRecordingVideo();
// ...
const path = await device.stopRecordingVideo();
```

### Recipe 11 — Flaky-resistant locators

```yaml
# Maestro — prefer text + testID
- tapOn:
    id: "submitButton"
    enabled: true
- assertVisible:
    text: "Order placed"
    visible: true
```

```js
// Detox — by.id over by.text when possible
await element(by.id("submitButton")).tap();
await waitFor(element(by.id("orderConfirmation"))).toBeVisible().withTimeout(10000);
```

### Recipe 12 — Tool selection rubric

```markdown
| Need | Tool |
|---|---|
| Fastest setup, YAML, multi-stack | Maestro |
| Pure React Native, lowest flakiness | Detox |
| Cross-language (Python/Java), hybrid app | Appium + WDIO |
| Cross-platform native | Maestro or Appium |
| Real-device cloud | BrowserStack App Live / Sauce Real Device Cloud |
| iOS-only native, Apple-blessed | XCUITest |
| Android-only native, Google-blessed | Espresso |
| Flutter | flutter_driver + Maestro Flutter |
```

## Examples

### Example 1: Greenfield RN app — Maestro from day 1

**Goal:** 0-test repo, ship login + onboarding tests by EOD.

1. `curl ... maestro | bash` (Recipe Setup).
2. `maestro studio` to record onboarding flow → save as `flows/onboarding.yaml`.
3. Write 3-5 happy-path flows manually (Recipe 1).
4. Add CI job (Recipe 7).
5. Run nightly on Android emulator + 1 real iOS device via cloud.

### Example 2: Stabilize flaky Appium suite

**Goal:** Existing Appium suite at 15% flake rate.

1. Audit selectors: `xpath` → `accessibility id` (testID) wherever possible.
2. Add explicit waits — `waitForElementToBeClickable` over hard sleeps.
3. Consider Detox for the React Native portion (Recipe 4) — drop flake to <2%.
4. Real-device matrix limited to top 3 (Recipe 6); emulator for the rest.

## Edge cases / gotchas

- **Detox iOS Sim builds slow** — pre-warm AVD / use simulator cache.
- **Appium server crashes** — pin `appium@2.x`; XCUITest driver pinned to
  match Xcode version.
- **Maestro element id vs text** — id preferred; text breaks under
  localization.
- **Permissions prompts** — auto-grant in Detox via `permissions`; Maestro
  uses `- runFlow: handlePermissions`.
- **Networking — real device on CI** — no Wi-Fi; use cellular profile or
  wired emulator. Real-device cloud has its own network.
- **iOS simulator dies after sleep** — kill + restart between tests in CI;
  detox restart helpers.
- **Android emulator slow on x86 vs ARM** — match host arch; M-series Mac =
  ARM AVD.
- **Maestro web mode** — supports web flows via Chrome DevTools; great for
  PWA tests.
- **Appium Inspector** — open the GUI to inspect element hierarchy; saves
  hours of debugging.
- **BrowserStack/Sauce cost** — per-minute billing; cap session duration.
- **Push notifications + cloud devices** — emulating via test driver is
  free; real push delivery needs APNS/FCM test credentials.
- **App size limit for cloud upload** — typically 1-2GB; pre-built debug APK
  is fine; release IPA larger may need split.

## Sources

- [Maestro docs](https://maestro.dev/docs)
- [Maestro CLI commands](https://maestro.dev/docs/cli/commands)
- [Detox](https://wix.github.io/Detox/)
- [Detox APIs](https://wix.github.io/Detox/docs/api/actions)
- [Appium 2](https://appium.io/docs/en/latest/)
- [WebdriverIO Appium](https://webdriver.io/docs/api/appium/)
- [BrowserStack App Live](https://www.browserstack.com/app-automate)
- [Sauce Real Device Cloud](https://docs.saucelabs.com/mobile-apps/automated-testing/)
- [Flutter driver](https://docs.flutter.dev/testing/integration-tests)
- [XCUITest](https://developer.apple.com/documentation/xctest)
- [Espresso](https://developer.android.com/training/testing/espresso)
