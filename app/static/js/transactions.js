document.addEventListener("DOMContentLoaded", function () {
  const depositBtn = document.getElementById("deposit-btn");
  const withdrawBtn = document.getElementById("withdraw-btn");
  const amountEntry = document.getElementById("amount-entry");
  const amountLabel = document.getElementById("amount-label");
  const amountDisplay = document.getElementById("amount-display");
  const amountInput = document.getElementById("amount-input");
  const amountKeypad = document.getElementById("amount-keypad");
  const amountCancel = document.getElementById("amount-cancel");
  const amountConfirm = document.getElementById("amount-confirm");
  const keys = amountKeypad.querySelectorAll(".key[data-key]");
  const successModal = document.getElementById("success-modal");
  const closeSuccessModal = document.getElementById("close-success-modal");
  const successMessage = document.getElementById("success-message");
  const errorModal = document.getElementById("error-modal");
  const closeErrorModal = document.getElementById("close-error-modal");
  const errorMessage = document.getElementById("error-message");
  const limitModal = document.getElementById("limit-modal");
  const closeLimitModal = document.getElementById("close-limit-modal");
  const limitMessage = document.getElementById("limit-message");

  let amountValue = "";
  let transactionType = "";

  function showAmountEntry(type) {
    transactionType = type;
    amountEntry.style.display = "flex";
    amountLabel.textContent = `Enter amount to ${type}:`;
    amountValue = "";
    updateAmountDisplay();
  }

  function updateAmountDisplay() {
    amountDisplay.innerHTML = amountValue || '<span class="pin-placeholder">0.00</span>';
    amountInput.value = amountValue;
  }

  depositBtn.addEventListener("click", function () {
    showAmountEntry("deposit");
  });

  withdrawBtn.addEventListener("click", function () {
    showAmountEntry("withdraw");
  });

  keys.forEach((key) => {
    key.addEventListener("click", function () {
      const keyVal = key.getAttribute("data-key");
      if (keyVal === ".") {
        if (!amountValue.includes(".")) {
          if (amountValue === "") amountValue = "0";
          amountValue += ".";
        }
      } else {
        // Limit to 2 decimal places
        if (amountValue.includes(".")) {
          const decimals = amountValue.split(".")[1];
          if (decimals.length >= 2) return;
        }
        amountValue += keyVal;
      }
      // Prevent leading zeros
      amountValue = amountValue.replace(/^0+(\d)/, "$1");
      updateAmountDisplay();
    });
  });

  amountCancel.addEventListener("click", function () {
    amountEntry.style.display = "none";
    amountValue = "";
    updateAmountDisplay();
  });

  amountConfirm.addEventListener("click", function () {
    if (!amountValue || isNaN(amountValue) || Number(amountValue) <= 0) {
      showErrorModal("Please enter a valid amount.");
      return;
    }
    fetch(`/account/transaction`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        type: transactionType,
        amount: parseFloat(amountValue).toFixed(2)
      })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        if (transactionType === "deposit") {
          showSuccessModal(`Your account is now: $${data.new_balance}`);
        } else if (transactionType === "withdraw") {
          showSuccessModal(`You withdrew: $${parseFloat(amountValue).toFixed(2)}<br>Your account is now: $${data.new_balance}`);
        }
      } else if (data.limit_exceeded) {
        showLimitModal(`Withdrawal limit exceeded.<br>Your limit is $${parseFloat(data.withdrawal_limit).toFixed(2)}.`);
      } else {
        showErrorModal(data.message || "Transaction failed.");
      }
    });
  });

  function showSuccessModal(message) {
    successMessage.innerHTML = message;
    successModal.style.display = "flex";
  }

  function showErrorModal(message) {
    errorMessage.innerHTML = message;
    errorModal.style.display = "flex";
    amountValue = "";
    updateAmountDisplay();
  }

  function showLimitModal(message) {
    limitMessage.innerHTML = message;
    limitModal.style.display = "flex";
    amountValue = "";
    updateAmountDisplay();
  }

  if (closeSuccessModal) {
    closeSuccessModal.onclick = function () {
      successModal.style.display = "none";
      window.location.reload();
    };
  }
  if (closeErrorModal) {
    closeErrorModal.onclick = function () {
      errorModal.style.display = "none";
    };
  }
  if (closeLimitModal) {
    closeLimitModal.onclick = function () {
      limitModal.style.display = "none";
    };
  }

  // Initialize display
  updateAmountDisplay();
});