✅ Step 1: Build the LTI Tool Backend (/lti/oidc, /lti/launch, /.well-known/jwks.json)

📌 Purpose:

Canvas uses the LTI 1.3 standard, which combines OpenID Connect for secure login and standardized data exchange.

You need to implement three critical endpoints:

Endpoint	Purpose	What Happens
/lti/oidc	Canvas sends login requests here	Triggered when users click your tool in Canvas
/lti/launch	Main entry point of your tool	Receives and validates identity token (JWT), then renders your UI
/.well-known/jwks.json	JWKS (public key) endpoint	Canvas uses this to verify JWT signatures

🧠 Concept:

Think of it like implementing a “Log in with Google” button – this is how you allow Canvas to securely launch your tool.

⸻

✅ Step 2: Write the JSON Tool Configuration (Describe What and Where)

📌 Purpose:

This JSON tells Canvas:
	•	What is your tool called?
	•	Where does it redirect to when clicked?
	•	What icon or text should be shown?
	•	Where should it appear (e.g., course_navigation)?

🧠 Concept:

It’s like writing a plugin manifest. Canvas uses this to recognize and place your tool correctly in the UI.

⸻

✅ Step 3: Register a Developer Key (Generate Client ID)

📌 Purpose:

You submit your JSON to Canvas as a Developer Key.
Once accepted, Canvas will generate a Client ID for your tool.

🧠 Concept:

Canvas is essentially saying:

	“Okay, I now officially recognize your tool. I’ll remember its metadata and allow it to be installed in courses.”

⸻

✅ Step 4: Install the Tool in a Course (Bind the Client ID)

📌 Purpose:

This installs your tool into a specific Canvas course so that users can access it.

Steps:
	1.	Go to the course → Settings → Apps tab
	2.	Click “View App Configurations” → “+ App”
	3.	Select “By Client ID” and paste your Client ID
	4.	Click Install

🧠 Concept:

This is like enabling a plugin for a specific page – you’ve registered it globally, but now you’re activating it per course.

⸻

✅ Step 5: Test Navigation Launch and SSO Login

📌 Purpose:

Verify the entire LTI 1.3 flow:
	•	Clicking “Encando” in the sidebar → triggers /lti/oidc
	•	Redirects to /lti/launch
	•	Your Encando page is rendered with the proper user and course context

🧠 Concept:

This proves the backend, security logic, and configuration are correctly wired with Canvas. You’ve completed a real SSO launch with contextual data.

⸻

🔁 End-to-End Flow Summary

[User clicks Encando navigation tab in Canvas]
        ↓
Canvas sends OIDC login request → POST to /lti/oidc
        ↓
Your tool verifies the request, receives JWT with user/context info
        ↓
Redirect to /lti/launch
        ↓
Render the Encando frontend page



⸻

🎯 Full Five-Step Summary

Step	Purpose	What Canvas Does
1. Backend Endpoints	Handle LTI login & launch, verify identity	Sends launch request, loads tool UI
2. JSON Config	Describe tool’s placement and behavior	Registers the tool metadata
3. Developer Key	Register tool into Canvas system	Generates a Client ID
4. Install in Course	Make the tool available in one or more courses	Adds navigation link to sidebar
5. Test SSO Launch	Verify full login + tool rendering	Launches your Encando UI with context
