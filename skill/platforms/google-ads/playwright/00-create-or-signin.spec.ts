/** Google Ads — Step 00: Sign in / create Google account. */
import { test, expect } from "@playwright/test";

test("00-create-or-signin", async ({ page }) => {
  await page.goto("https://accounts.google.com/signin");
  await page.waitForURL(/myaccount\.google\.com|accounts\.google\.com\/signin\/oauth/, { timeout: 5 * 60_000 });
  await expect(page).toHaveURL(/google\.com/);
});
