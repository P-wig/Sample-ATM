document.addEventListener("DOMContentLoaded", function () {
  const pinInput = document.getElementById("pin");
  const pinDisplay = document.getElementById("pin-display");
  const form = document.getElementById("login-form");
  const keys = document.querySelectorAll(".key[data-key]");
  const cancelBtn = document.getElementById("cancel");
  const confirmBtn = document.getElementById("confirm");
  const errorModal = document.getElementById("error-modal");
  const closeModal = document.getElementById("close-modal");
  const errorFlag = document.getElementById("error-flag");

  let pinValue = "";

  function updatePinDisplay() {
    pinDisplay.innerHTML = "";
    for (let i = 0; i < 4; i++) {
      if (i < pinValue.length) {
        const span = document.createElement("span");
        span.className = "pin-char";
        span.textContent = pinValue[i];
        pinDisplay.appendChild(span);
      } else {
        const span = document.createElement("span");
        span.className = "pin-placeholder";
        span.textContent = "-";
        pinDisplay.appendChild(span);
      }
    }
    pinInput.value = pinValue;
  }

  keys.forEach((key) => {
    key.addEventListener("click", function () {
      if (pinValue.length < 4) {
        pinValue += key.getAttribute("data-key");
        updatePinDisplay();
      }
    });
  });

  cancelBtn.addEventListener("click", function () {
    pinValue = "";
    updatePinDisplay();
  });

  confirmBtn.addEventListener("click", function () {
    if (pinValue.length === 4) {
      form.submit();
    } else {
      showErrorModal();
    }
  });

  function showErrorModal() {
    pinValue = "";
    updatePinDisplay();
    errorModal.style.display = "flex";
  }

  if (errorFlag && errorFlag.textContent === "1") {
    showErrorModal();
  }

  if (closeModal) {
    closeModal.onclick = function () {
      errorModal.style.display = "none";
    };
  }

  // Initialize display
  updatePinDisplay();
});