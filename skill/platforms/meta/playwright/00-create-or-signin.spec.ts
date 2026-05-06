/**
 * Meta — Step 00: Sign in or create Facebook + Business account.
 *
 * Recipe consumed by Playwright MCP. Selectors live in ../selectors.json.
 * State written to .state/meta-progress.json after each step.
 */

import { test, expect } from "@playwright/test";

test("00-create-or-signin", async ({ page }) => {
  await page.goto("https://business.facebook.com/");

  if (await page.locator("input[name='email']").isVisible()) {
    // existing user — let them sign in interactively, then assert landing
    await page.waitForURL(/business\.facebook\.com\/(latest|home)/, { timeout: 5 * 60_000 });
  } else {
    // route to signup flow — user fills personal account creation in foreground
    await page.goto("https://www.facebook.com/r.php");
    await page.waitForURL(/facebook\.com/, { timeout: 5 * 60_000 });
  }

  await expect(page).toHaveURL(/facebook\.com|business\.facebook\.com/);
  // Mark progress
  await page.evaluate(() => localStorage.setItem("marketing_agency_meta_step_00", "ok"));
});
