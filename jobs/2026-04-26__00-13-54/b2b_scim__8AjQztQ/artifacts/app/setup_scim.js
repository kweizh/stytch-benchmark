const fs = require("fs/promises");
const stytch = require("stytch");

async function main() {
  const { STYTCH_PROJECT_ID, STYTCH_SECRET } = process.env;

  if (!STYTCH_PROJECT_ID || !STYTCH_SECRET) {
    throw new Error("Missing STYTCH_PROJECT_ID or STYTCH_SECRET environment variables.");
  }

  const client = new stytch.B2BClient({
    project_id: STYTCH_PROJECT_ID,
    secret: STYTCH_SECRET,
  });

  const slug = `acme-scim-org-${Date.now()}`;

  const organization = await client.organizations.create({
    organization_name: "Acme SCIM Org",
    organization_slug: slug,
  });

  const connection = await client.scim.connection.create({
    organization_id: organization.organization_id,
    display_name: "Acme SCIM Connection",
    identity_provider: "okta",
  });

  const output = {
    organization_id: organization.organization_id,
    connection_id: connection.connection_id,
    base_url: connection.base_url,
    bearer_token: connection.bearer_token,
  };

  await fs.writeFile(
    "/home/user/app/scim_output.json",
    JSON.stringify(output, null, 2),
    "utf8"
  );

  console.log("SCIM connection created. Output written to scim_output.json");
}

main().catch((error) => {
  console.error("Failed to set up SCIM connection:", error);
  process.exit(1);
});
