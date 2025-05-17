function processCode() {
    const code = document.getElementById("code-input").value;
    const errorMessage = document.getElementById("error-message");

    // Clear any previous error message
    errorMessage.style.display = "none";
    errorMessage.textContent = "";

    // Validate input
    if (!code.trim()) {
        errorMessage.style.display = "block";
        errorMessage.textContent = "Please enter some code!";
        return;
    }

    // Send code to backend using AJAX (Fetch API)
    fetch('http://127.0.0.1:5000/lexer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "code": code })
    })
    .then(response => response.json())
    .then(data => {
        // Display tokens
        if (data.tokens && data.tokens.length > 0) {
            displayTokens(data.tokens);

            // Send tokens to parser
            sendToParser(data.tokens);
        } else {
            displayError("Lexer failed: Unable to tokenize the input.");
        }
    })
    .catch(error => {
        displayError("Error: " + error.message);
    });
}

function displayTokens(tokens) {
    const tokenStreamDiv = document.getElementById("token-stream");
    tokenStreamDiv.innerHTML = ""; // Clear previous tokens

    const table = document.createElement("table");
    table.innerHTML = `<thead><tr><th>Type</th><th>Value</th></tr></thead><tbody></tbody>`;

    tokens.forEach(token => {
        const row = document.createElement("tr");
        row.innerHTML = `<td>${token.type}</td><td>${token.value}</td>`;
        table.querySelector("tbody").appendChild(row);
    });

    tokenStreamDiv.appendChild(table);
}

function sendToParser(tokens) {
    fetch('http://127.0.0.1:5000/parser', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "tokens": tokens })
    })
    .then(response => response.json())
    .then(data => {
        if (data.parse_tree) {
            displayParseTree(data.parse_tree);
        } else {
            displayError("Parser failed: Invalid syntax.");
        }
    })
    .catch(error => {
        displayError("Error: " + error.message);
    });
}

function displayParseTree(parseTree) {
    const parseTreeDiv = document.getElementById("parse-tree");
    parseTreeDiv.innerHTML = JSON.stringify(parseTree, null, 2); // Display as formatted JSON
}

function displayError(message) {
    const errorMessage = document.getElementById("error-message");
    errorMessage.style.display = "block";
    errorMessage.textContent = message;
}
