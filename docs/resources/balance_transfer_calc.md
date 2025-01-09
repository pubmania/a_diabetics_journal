---
title: Balance Transfer Calculator
hide:
    - toc
---
<script>
    function calculateTransfer() {
        // Get user input values
        let amountToTransfer = parseFloat(document.getElementById("amountToTransfer").value);
        const balanceTransferFee = parseFloat(document.getElementById("balanceTransferFee").value);
        const balanceTransferDuration = parseInt(document.getElementById("balanceTransferDuration").value);
        const plannedMonthlyPayment = parseFloat(document.getElementById("plannedMonthlyPayment").value);
        // Check if any fields are empty
        if (!amountToTransfer || !balanceTransferFee || !balanceTransferDuration || !plannedMonthlyPayment) {
            document.getElementById("result").innerHTML = "<strong style='color: red;'>Please fill in all fields.</strong>";
            return; // Exit the function if validation fails
        }
        // Initialise Variables
        let totalTimeToPay = 0;
        let feePaid = 0;
        const initialAmountToTransfer = amountToTransfer;

        while (amountToTransfer > plannedMonthlyPayment) {
            let amountTransferred = amountToTransfer * (1 + balanceTransferFee / 100);
            let totalTimeRequired = amountTransferred / plannedMonthlyPayment;

            if (totalTimeRequired > balanceTransferDuration) {
                feePaid += amountToTransfer * (balanceTransferFee / 100);
                amountToTransfer = amountTransferred - (plannedMonthlyPayment * balanceTransferDuration);
                totalTimeToPay += balanceTransferDuration;
            } else {
                totalTimeToPay += totalTimeRequired;
                amountToTransfer = amountTransferred - (plannedMonthlyPayment * totalTimeRequired);
            }
        }

        // Display results
        const result = `
            To pay off <strong>£${initialAmountToTransfer}</strong> using monthly payments of <strong>£${plannedMonthlyPayment}</strong> with a <strong>${balanceTransferDuration} months</strong> balance transfer renewed until the whole amount is paid off and each renewal has a balance transfer fee of <strong>${balanceTransferFee} %</strong>, one will pay a total fee of <strong>£${feePaid.toFixed(2)}</strong> and will need to make the monthly payment for <strong>${Math.round(totalTimeToPay)} months</strong>. 
            
            Balance transfer will need to be renewed at least <strong>${Math.round(totalTimeToPay / balanceTransferDuration)} times</strong>.
        `;
        document.getElementById("result").innerHTML = result;
    }
</script>

## Balance Transfer Calculator

<div class="grid cards" markdown>
-   **Amount to Transfer (£):** 
  
    --- 
  
    <input class="md-input" type="number" id="amountToTransfer" required>

-   **Balance Transfer Fee (%):** 
  
    --- 
  
    <input class="md-input" type="number" id="balanceTransferFee" required>

</div>

<div class="grid cards" markdown>
-   **Balance Transfer Duration (months):**
  
    --- 
  
    <input class="md-input" type="number" id="balanceTransferDuration" required>

-   **Planned Monthly Payment (£):** 
  
    --- 

    <input class="md-input" type="number" id="plannedMonthlyPayment" required>

</div>

<p align="center"><a class="md-button" onclick="calculateTransfer()">Calculate <span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M7 2h10a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2m0 2v4h10V4zm0 6v2h2v-2zm4 0v2h2v-2zm4 0v2h2v-2zm-8 4v2h2v-2zm4 0v2h2v-2zm4 0v2h2v-2zm-8 4v2h2v-2zm4 0v2h2v-2zm4 0v2h2v-2z"></path></svg></span></a></p>


<p id="result"></p>

