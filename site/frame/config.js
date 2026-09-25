// SkyWays Architect · site configuration.
// Read by frame/frame.js. Nothing in this file is secret; it is served to every visitor.
window.SKYWAYS_SITE = {
  author: "Akash Das",
  // The tool's own name, used in the footer's first sentence and the drawer.
  siteName: "The SkyWays PDLC Simulator",
  year: 2026,
  links: {
    repo: "https://github.com/akash-coded/aws-bedrock-agentcore-strands",
    ideas: "https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/101",
    discussions: "https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions",
    issues: "https://github.com/akash-coded/aws-bedrock-agentcore-strands/issues/new/choose",
    license: "https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/LICENSE",
    source: "https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/site/app/SkyWays-Architect.html",
    frameless: "app/SkyWays-Architect.html",
    // The manual this tool belongs to, relative to the framed copy at /simulator/. Empty = no way back.
    manual: "../",
    manualPages: [["Learn", "../learn/"], ["Roles", "../product-manager/"], ["Templates", "../templates/"],
                  ["Prompts", "../prompts/"], ["Mental models", "../models/"]]
  },
  // How the contact form delivers messages.
  //   endpoint  – leave empty and the form opens the visitor's mail app with the message ready to send.
  //               Set it to the Function URL printed by site/contact-relay/deploy.sh (e-mail + private log),
  //               or to a Formspree / Web3Forms form URL if you prefer a hosted service.
  //   accessKey – Web3Forms only; ignored otherwise.
  //   mailto    – the fallback address, kept in two parts so naive scrapers do not harvest it.
  contact: {
    endpoint: "",
    accessKey: "",
    mailto: ["mfs.akash", "gmail.com"]
  }
};
