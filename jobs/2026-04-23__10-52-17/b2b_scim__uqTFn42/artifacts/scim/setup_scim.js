const fs = require("fs/promises");
const stytch = require("stytch");

async function main() {
  const projectId = process.env.STYTCH_PROJECT_ID;
  const secret = process.env.STYTCH_SECRET;

  if (!projectId || !secret) {
    throw new Error("STYTCH_PROJECT_ID and STYTCH_SECRET must be set in the environment.");
  }

  const client = new stytch.B2BClient({
    project_id: projectId,
    secret,
  });

  const timestamp = Date.now();
  const organizationSlug = `acme-scim-org-${timestamp}`;

  const organization = await client.organizations.create({
    organization_name: "Acme SCIM Org",
    organization_slug: organizationSlug,
  });

  const scimConnection = await client.scim.connection.create({
    organization_id: organization.organization_id,
    display_name: "Acme SCIM Connection",
    identity_provider: "okta",
  });

  const output = {
    organization_id: organization.organization_id,
    connection_id: scimConnection.connection_id,
    base_url: scimConnection.base_url,
    bearer_token: scimConnection.bearer_token,
  };

  await fs.writeFile("/home/user/app/scim_output.json", `${JSON.stringify(output, null, 2)}\n`, "utf8");

  console.log("SCIM connection created. Output saved to /home/user/app/scim_output.json");
}

main().catch((error) => {
  console.error("Failed to setup SCIM connection:", error);
  process.exit(1);
});
