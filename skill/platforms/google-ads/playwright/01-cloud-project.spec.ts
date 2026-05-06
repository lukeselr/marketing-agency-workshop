/** Google Ads — Step 01: Google Cloud project (foundation for OAuth). */
import { test, expect } from "@playwright/test";

test("01-cloud-project", async ({ page }) => {
  await page.goto("https://console.cloud.google.com/projectcreate");
  await page.getByLabel(/Project name/i).fill(process.env.MA_GCP_PROJECT_NAME || "marketing-agency");
  await page.getByRole("button", { name: /Create/i }).click();
  await page.waitForURL(/project=([\w-]+)/, { timeout: 60_000 });
  const projectId = page.url().match(/project=([\w-]+)/)?.[1] ?? "";
  expect(projectId.length).toBeGreaterThan(3);
  process.stdout.write(JSON.stringify({ gcp_project_id: projectId }) + "\n");
});
