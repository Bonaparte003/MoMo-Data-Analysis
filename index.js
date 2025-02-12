document.addEventListener("DOMContentLoaded", function () {
  const logo = document.querySelector(".logo");
  const navLinks = document.querySelectorAll(".nav-link");
  const navLinkTexts = document.querySelectorAll(".nav-link p");
  const home = document.querySelector(".home-section");
  const addFile = document.querySelector(".Add-file-section");
  const print = document.querySelector(".print-section");
  const budget = document.querySelector(".budget-section");
  const bot = document.querySelector(".bot-section");
  const settings = document.querySelector(".settings-section");
  const fileInput = document.getElementById("file");
  let file_content = "";
  let table = document.getElementById("table");
  const transaction_types = document.querySelectorAll(".transaction-type a");
  let currentTableType = "cashpower";
  let databaseData = {};
  let totaldata;
  let airtime = [];
  let bundles = [];
  let cashpower = [];
  let codeholders = [];
  let deposit = [];
  let failed = [];
  let incoming = [];
  let nontransaction = [];
  let payments = [];
  let reversedtransactions = [];
  let thirdparty = [];
  let transfer = [];
  let withdraw = [];
  let cashIn;
  let cashOut;
  let fees;
  let balance;

  document.querySelector('.nav-link-print').addEventListener('click', function() {
    window.print();
});

//

// Handle budget form submission
const budgetForm = document.getElementById('budget-form');
const budgetTableBody = document.querySelector('#budget-table tbody');

budgetForm.addEventListener('submit', function(event) {
    event.preventDefault();

    const item = document.getElementById('item').value;
    const amount = document.getElementById('amount').value;

    // Create a new row for the budget item
    const row = document.createElement('tr');
    const itemCell = document.createElement('td');
    const amountCell = document.createElement('td');

    itemCell.textContent = item;
    amountCell.textContent = amount;

    row.appendChild(itemCell);
    row.appendChild(amountCell);

    // Add the new row to the table
    budgetTableBody.appendChild(row);

    // Clear the form
    budgetForm.reset();
});

  // Function to show loading overlay
  function showLoading(message) {
    let loadingDiv = document.getElementById("loading-overlay");
    if (!loadingDiv) {
      loadingDiv = document.createElement("div");
      loadingDiv.id = "loading-overlay";
      loadingDiv.innerHTML = `<div class="loading-message">${message}</div>`;
      document.body.appendChild(loadingDiv);
    }
    loadingDiv.style.display = "flex";
  }

  // Function to hide loading overlay
  function hideLoading() {
    const loadingDiv = document.getElementById("loading-overlay");
    if (loadingDiv) {
      loadingDiv.style.display = "none";
    }
  }

  // Function to show a section
  function showSection(sectionToShow) {
    const sections = [home, addFile, print, budget, bot, settings];
    sections.forEach((section) => (section.style.display = "none"));
    sectionToShow.style.display = "flex";
  }

  // Function to activate navigation link
  function activateNavLink(navLinkToActivate) {
    navLinks.forEach((navLink) =>
      navLink.classList.remove("nav-link_activated")
    );
    navLinkToActivate.classList.add("nav-link_activated");
  }

  // Function to hide/show text
  function hideInfo() {
    navLinkTexts.forEach((navLinkText) => {
      navLinkText.style.display =
        navLinkText.style.display === "none" ? "flex" : "none";
    });
  }

  // Function to show alert messages
  function showAlert(message, isError = false) {
    const alertBox = document.createElement("div");
    alertBox.className = `custom-alert ${isError ? "error" : ""}`;
    alertBox.textContent = message;
    document.body.appendChild(alertBox);
    alertBox.classList.add("show");
    setTimeout(() => {
      alertBox.classList.remove("show");
      document.body.removeChild(alertBox);
    }, 3000);
  }

  // Function to fetch database results
  async function fetchDatabaseResults() {
    showLoading("Fetching database results...");
    try {
      const databaseResponse = await fetch(
        "http://127.0.0.1:8000/database_return"
      );
      if (!databaseResponse.ok) throw new Error("Database fetch failed.");

      databaseData = await databaseResponse.json(); // Update the global variable
      hideLoading();
      console.log("Database data:", databaseData); // Log the API response

      // Assign data to arrays
      airtime = databaseData.airtime || [];
      bundles = databaseData.bundles || [];
      cashpower = databaseData.cashpower || [];
      codeholders = databaseData.codeholders || [];
      deposit = databaseData.deposit || [];
      failed = databaseData.failedtransactions || [];
      incoming = databaseData.incomingmoney || [];
      nontransaction = databaseData.nontransaction || [];
      payments = databaseData.payments || [];
      reversedtransactions = databaseData.reversedtransactions || [];
      thirdparty = databaseData.thirdparty || [];
      transfer = databaseData.transfer || [];
      withdraw = databaseData.withdraw || [];

      table_creator(); // Create and display table
    } catch (error) {
      hideLoading();
      showAlert(`Error fetching database: ${error.message}`, true);
    }
  }

  // Handle file upload and database fetch
  fileInput.addEventListener("change", async function (event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async function (e) {
      file_content = e.target.result;
      alert("File uploaded successfully!");

      if (file_content) {
        showLoading("Uploading file...");
        try {
          const response = await fetch("http://127.0.0.1:8000/file", {
            method: "POST",
            headers: { "Content-Type": "text/plain" },
            body: file_content
          });
          alert("Uploaded");

          if (!response.ok) throw new Error("File upload failed.");

          const responseData = await response.json();
          hideLoading();
          showAlert("File uploaded successfully!");

          // Fetch database results after file upload and database reconfiguration
          fetchDatabaseResults();
        } catch (error) {
          hideLoading();
          showAlert(`Error: ${error.message}`, true);
        }
      }
    };
    reader.readAsText(file);
  });

  // Function to create and display table
  function table_creator() {
    totaldata = databaseData.data;
    airtime = totaldata.airtime || [];
    bundles = totaldata.bundles || [];
    cashpower = totaldata.cashpower || [];
    codeholders = totaldata.codeholders || [];
    deposit = totaldata.deposit || [];
    failed = totaldata.failedtransactions || [];
    incoming = totaldata.incomingmoney || [];
    nontransaction = totaldata.nontransaction || [];
    payments = totaldata.payments || [];
    reversedtransactions = totaldata.reversedtransactions || [];
    thirdparty = totaldata.thirdparty || [];
    transfer = totaldata.transfer || [];
    withdraw = totaldata.withdraw || [];
    tableContainer = document.getElementById("table");
    tableContainer.innerHTML = ""; // Clear existing table

    const createTable = (data) => {
      const table = document.createElement("table");
      const thead = document.createElement("thead");
      const tbody = document.createElement("tbody");

      // Create table header
      const headerRow = document.createElement("tr");
      const columns = Object.keys(data[0] || {});
      columns.forEach((col) => {
        const th = document.createElement("th");
        th.textContent = col;
        headerRow.appendChild(th);
      });
      thead.appendChild(headerRow);

      // Create table rows
      data.forEach((row) => {
        const tr = document.createElement("tr");
        columns.forEach((col) => {
          const td = document.createElement("td");
          td.textContent = row[col] || "";
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });

      table.appendChild(thead);
      table.appendChild(tbody);
      return table;
    };

    const displayTable = (data) => {
      const table = createTable(data);
      tableContainer.appendChild(table);
    };

    // Example: Display cashpower table on load
    displayTable(cashpower);

    // Add event listeners for other transaction types
    document.querySelector(".cashpower").addEventListener("click", () => {
      tableContainer.innerHTML = ""; // Clear existing table
      displayTable(cashpower);
      setActiveButton(".cashpower");
    });
    document.querySelector(".codeholders").addEventListener("click", () => {
      tableContainer.innerHTML = ""; // Clear existing table
      displayTable(codeholders);
      setActiveButton(".codeholders");
    });
    document.querySelector(".airtime").addEventListener("click", () => {
      tableContainer.innerHTML = ""; // Clear existing table
      displayTable(airtime);
      setActiveButton(".airtime");
    });
    document.querySelector(".bundles").addEventListener("click", () => {
      tableContainer.innerHTML = ""; // Clear existing table
      displayTable(bundles);
      setActiveButton(".bundles");
    });
    document.querySelector(".incomingmoney").addEventListener("click", () => {
      tableContainer.innerHTML = ""; // Clear existing table
      displayTable(incoming);
      setActiveButton(".incomingmoney");
    });
    document.querySelector(".nontransaction").addEventListener("click", () => {
      tableContainer.innerHTML = ""; // Clear existing table
      displayTable(nontransaction);
      setActiveButton(".nontransaction");
    });
    document.querySelector(".deposit").addEventListener("click", () => {
      tableContainer.innerHTML = ""; // Clear existing table
      displayTable(deposit);
      setActiveButton(".deposit");
    });
    document
      .querySelector(".failedtransactions")
      .addEventListener("click", () => {
        tableContainer.innerHTML = ""; // Clear existing table
        displayTable(failed);
        setActiveButton(".failedtransactions");
      });
    document.querySelector(".thirdparty").addEventListener("click", () => {
      tableContainer.innerHTML = ""; // Clear existing table
      displayTable(thirdparty);
      setActiveButton(".thirdparty");
    });
    document.querySelector(".transfer").addEventListener("click", () => {
      tableContainer.innerHTML = ""; // Clear existing table
      displayTable(transfer);
      setActiveButton(".transfer");
    });
    document.querySelector(".payments").addEventListener("click", () => {
      tableContainer.innerHTML = ""; // Clear existing table
      displayTable(payments);
      setActiveButton(".payments");
    });
    document
      .querySelector(".reversedtransactions")
      .addEventListener("click", () => {
        tableContainer.innerHTML = ""; // Clear existing table
        displayTable(reversedtransactions);
        setActiveButton(".reversedtransactions");
      });
    document.querySelector(".withdraw").addEventListener("click", () => {
      tableContainer.innerHTML = ""; // Clear existing table
      displayTable(withdraw);
      setActiveButton(".withdraw");
    });
  }

  // Function to update financial overview
  function updateFinancialOverview() {
    // Reset values to zero
    cashIn = 0;
    cashOut = 0;
    fees = 0;

    const arraysToCheck = [
      deposit,
      incoming,
      thirdparty,
      reversedtransactions,
      payments,
      airtime,
      bundles,
      cashpower,
      codeholders,
      transfer,
      withdraw
    ];

    arraysToCheck.forEach((array) => {
      if (!Array.isArray(array)) {
        console.error("Expected an array but got:", array);
        return;
      }
    });

    for (let i = 0; i < deposit.length; i++) {
      if (deposit[i] && deposit[i].Amount) {
        cashIn += deposit[i].Amount;
        console.log(deposit[i].Amount);
      }
    }
    for (let i = 0; i < incoming.length; i++) {
      if (incoming[i] && incoming[i].Amount) {
        cashIn += incoming[i].Amount;
      }
    }
    for (let i = 0; i < thirdparty.length; i++) {
      if (thirdparty[i] && thirdparty[i].Amount) {
        cashIn += thirdparty[i].Amount;
        console.log(thirdparty[i].Amount);
      }
    }
    for (let i = 0; i < reversedtransactions.length; i++) {
      if (reversedtransactions[i] && reversedtransactions[i].Amount) {
        cashIn += reversedtransactions[i].Amount;
      }
    }
    for (let i = 0; i < payments.length; i++) {
      if (payments[i] && payments[i].Amount) {
        cashOut += payments[i].Amount;
      }
    }
    for (let i = 0; i < airtime.length; i++) {
      if (airtime[i] && airtime[i].Amount) {
        cashOut += airtime[i].Amount;
      }
    }
    for (let i = 0; i < bundles.length; i++) {
      if (bundles[i] && bundles[i].Amount) {
        cashOut += bundles[i].Amount;
      }
    }
    for (let i = 0; i < cashpower.length; i++) {
      if (cashpower[i] && cashpower[i].Amount) {
        cashOut += cashpower[i].Amount;
      }
    }
    for (let i = 0; i < codeholders.length; i++) {
      if (codeholders[i] && codeholders[i].Amount) {
        cashOut += codeholders[i].Amount;
      }
    }
    for (let i = 0; i < transfer.length; i++) {
      if (transfer[i] && transfer[i].Amount) {
        cashOut += transfer[i].Amount;
      }
    }
    for (let i = 0; i < withdraw.length; i++) {
      if (withdraw[i] && withdraw[i].Amount) {
        cashOut += withdraw[i].Amount;
      }
    }

    for (let i = 0; i < payments.length; i++) {
      if (payments[i] && payments[i].Fee) {
        fees += payments[i].Fee;
      }
    }
    for (let i = 0; i < withdraw.length; i++) {
      if (withdraw[i] && withdraw[i].Fee) {
        fees += withdraw[i].Fee;
      }
    }
    balance = cashIn - cashOut - fees;
    console.log(cashIn, cashOut, fees, balance);

    document.querySelector(".cash_in p").textContent = cashIn.toFixed(2);
    document.querySelector(".cash_out p").textContent = cashOut.toFixed(2);
    document.querySelector(".fees p").textContent = fees.toFixed(2);
    document.querySelector(".balance p").textContent = balance.toFixed(2);
  }

  // Function to set active button
  function setActiveButton(selector) {
    transaction_types.forEach((transaction_type) => {
      transaction_type.classList.remove("active");
    });
    document.querySelector(selector).classList.add("active");
  }

  // Function to filter table based on search and date
  function filterTable() {
    const searchInput = document
      .querySelector(".search input")
      .value.toLowerCase();
    const dateInput = document.querySelector(".calendar input").value;
    const filteredData = databaseData.data[currentTableType].filter((item) => {
      const matchesSearch =
        !searchInput ||
        (item.receiver && item.receiver.toLowerCase().includes(searchInput)) ||
        (item.txid && item.txid.toLowerCase().includes(searchInput)) ||
        (item.sender && item.sender.toLowerCase().includes(searchInput));
      const matchesDate = !dateInput || item.date === dateInput;
      return matchesSearch && matchesDate;
    });
    displayTable(filteredData);
  }

  // Add event listeners for search and date filter
  document
    .querySelector(".search input")
    .addEventListener("input", filterTable);
  document
    .querySelector(".calendar input")
    .addEventListener("change", filterTable);

  // Handle navigation clicks
  logo.addEventListener("click", hideInfo);
  navLinks.forEach((navLink, index) => {
    navLink.addEventListener("click", () => {
      activateNavLink(navLink);
      const sections = [home, addFile, print, budget, bot, settings];
      showSection(sections[index]);
    });
  });

  //Event listener for transaction types
  transaction_types.forEach((transaction_type) => {
    transaction_type.addEventListener("click", () => {
      currentTableType = transaction_type.dataset.type;
      table_creator(databaseData, currentTableType);
    });
  });

  document.getElementById("file").addEventListener("change", function (event) {
    const file = event.target.files[0];
    const errorElement = document.getElementById("file-error");
    if (file && file.type !== "text/xml") {
      errorElement.style.display = "block";
      event.target.value = ""; // Clear the input
    } else {
      errorElement.style.display = "none";
    }
  });
  // Add event listener for the print button
  // document
  //   .querySelector(".nav-link-print")
  //   .addEventListener("click", function () {
  //     window.print();
  //   });
  // Set initial section
  showSection(addFile);
  activateNavLink(navLinks[1]);
  fetchDatabaseResults();
  table_creator();
  updateFinancialOverview();
});
