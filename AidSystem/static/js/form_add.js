
    function toggleAidFields() {
        const aidType = document.getElementById("aidType").value;
        document.getElementById("amountDiv").style.display = aidType === "قيمة مالية" ? "block" : "none";
        document.getElementById("otherDiv").style.display = aidType === "اخرى" ? "block" : "none";
    }

    function handleMaritalStatus() {
      const status = document.getElementById("maritalStatus").value;
      const wivesSection = document.getElementById("wivesSection");

      if (status === "متزوج") {
        wivesSection.style.display = "block";
        handleWivesCount();
      } else {
        wivesSection.style.display = "none";
      }
    }

    function handleWivesCount() {
      const count = parseInt(document.getElementById("wivesCount").value);
      for (let i = 1; i <= 4; i++) {
        document.getElementById("wife" + i).style.display = i <= count ? "block" : "none";
      }
    }

    document.getElementById('injuredSelect').addEventListener('change', function () {
      const injuredValue = this.value;
      const injuredInput = document.getElementById('injuredCount');
      if (injuredValue === 'نعم') {
        injuredInput.min = 1;
        if (injuredInput.value < 1) injuredInput.value = 1;
      } else {
        injuredInput.min = 0;
        injuredInput.value = 0;
      }
    });
 


    