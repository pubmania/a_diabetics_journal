---
title: HbA1c and BG Unit Converter
hide:
  - toc
---

<div class="grid cards">
	<ul>
		<li>
			<h3 id="hba1c">HbA1c</h3>
			<hr>
			<div class="grid cards" markdown=""><ul>
				<li>
					<p><strong>DCCT</strong></p>
					<hr>
					<p><input type="number" step="0.1" id="dcct" class="md-input" onchange="update_using_dcct()"> <strong>% (Percent)</strong></p>
				</li>
				<li>
					<p><strong>IFCC</strong></p>
					<hr>
					<p><input type="number" step="0.1" id="ifcc" class="md-input" onchange="update_using_ifcc()"> <strong>mmol/mol</strong></p>
				</li>
			</ul></div>
		</li>
		<li>
			<h3 id="average-blood-glucose">Average Blood Glucose<a class="headerlink localLink" href="#average-blood-glucose" title="Permanent link">¶</a></h3>
			<hr>
			<div class="grid cards" markdown=""><ul>
			<li>
				<p><strong>Milligram per decilitre</strong></p>
				<hr>
				<p><input type="number" step="0.1" id="mg_dl" class="md-input" onchange="update_using_mg_dl()"><strong>mg/dl</strong></p>
			</li>
			<li>
				<p><strong>Millimole per litre</strong></p>
				<hr>
				<p><input type="number" step="0.1" id="mmol_l" class="md-input" onchange="update_using_mmol_l()"> <strong>mmol/l</strong></p>
			</li>
			</ul></div>
		</li>
	</ul>
</div>
<div>
	<p><span id="err_mess" style="color: red"></span></p>
</div>


!!! site-info "Info"
    Following conversion formula[^1] is used: 
    [^1]: Some explanation is available on [NGSP Site](https://ngsp.org/ifcc.asp):

    ```
    IFCC = (DCCT - 2.15) * 10.929
    ```
    
    This is an approximation for conversion based on what I understand. 
    
    Additionally, an approximation of Average Blood Glucose based on DCCT HbA1c value are calculated using following formula:
    
    ```
    Average Blood Glucose (mg/dl) = (A1C * 28.7) - 46.7
    Average Blood Glucose (mmol/l) = (A1C * 1.59) - 2.04
    ```

    Finally, entering value in one of the unit fields will also provide conversion to other unit using the formula as well as provide HbA1c values assuming the provided value is average BG measure in given unit:

    ```
    BG in mg/dl = BG in mmol/l * 18
    ```

<script>
function update_using_dcct() {
    var dcct_value = parseFloat(document.getElementById("dcct").value);
    if (isNaN(dcct_value)) {
    document.getElementById("ifcc").value = "";
    document.getElementById("err_mess").innerText = "";
    document.getElementById("mg_dl").value = "";
    document.getElementById("mmol_l").value = "";
    } else {
    if(validatedcct()){
    document.getElementById("ifcc").value = ((dcct_value - 2.15) * 10.929).toFixed(2);
    document.getElementById("mg_dl").value = ((dcct_value * 28.7) - 46.7).toFixed(2);
    document.getElementById("mmol_l").value = ((dcct_value * 1.59) - 2.04).toFixed(2);
    document.getElementById("err_mess").innerText = "";
    }
    }
}

function update_using_ifcc() {
    var ifcc_value = parseFloat(document.getElementById("ifcc").value);
    if (isNaN(ifcc_value)) {
    document.getElementById("dcct").value = "";
    document.getElementById("err_mess").innerText = "";
    document.getElementById("mg_dl").value = "";
    document.getElementById("mmol_l").value = "";
    } else {
    if (validateifcc()) {
    document.getElementById("dcct").value = ((ifcc_value / 10.929) + 2.15).toFixed(2);
    document.getElementById("mg_dl").value = ((((ifcc_value / 10.929) + 2.15) * 28.7) - 46.7).toFixed(2);
    document.getElementById("mmol_l").value = ((((ifcc_value / 10.929) + 2.15) * 1.59) - 2.04).toFixed(2);
    document.getElementById("err_mess").innerText = "";
    }
    }
}

function update_using_mg_dl() {
    var mg_dl_value = parseFloat(document.getElementById("mg_dl").value);
    if (isNaN(mg_dl_value)) {
    document.getElementById("dcct").value = "";
    document.getElementById("err_mess").innerText = "";
    document.getElementById("ifcc").value = "";
    document.getElementById("mmol_l").value = "";
    } else {
    if (validate_mg_dl()) {
    document.getElementById("dcct").value = ((mg_dl_value+46.7)/28.7).toFixed(2);
    document.getElementById("ifcc").value = ((((mg_dl_value+46.7)/28.7) - 2.15) * 10.929).toFixed(2);
    document.getElementById("mmol_l").value = (mg_dl_value/18).toFixed(2);
    document.getElementById("err_mess").innerText = "";
    }
    }
}

function update_using_mmol_l() {
    var mmol_l_value = parseFloat(document.getElementById("mmol_l").value);
    if (isNaN(mmol_l_value)) {
    document.getElementById("dcct").value = "";
    document.getElementById("err_mess").innerText = "";
    document.getElementById("ifcc").value = "";
    document.getElementById("mg_dl").value = "";
    } else {
    if (validate_mmol_l()) {
    document.getElementById("dcct").value = (((mmol_l_value*18)+46.7)/28.7).toFixed(2);
    document.getElementById("ifcc").value = (((((mmol_l_value*18)+46.7)/28.7) - 2.15) * 10.929).toFixed(2);
    document.getElementById("mg_dl").value = (mmol_l_value*18).toFixed(2);
    document.getElementById("err_mess").innerText = "";
    }
    }
}

function validatedcct() {
    var dcct_value = parseFloat(document.getElementById("dcct").value);
    if (isNaN(dcct_value) || dcct_value < 2.5 || dcct_value > 24) {
    document.getElementById("dcct").value = "";
    document.getElementById("err_mess").innerText = "Enter a value between 2.5 and 24 for DCCT";
    document.getElementById("ifcc").value = "";
    document.getElementById("mg_dl").value = "";
    document.getElementById("mmol_l").value = "";
    return 0
    } else {
    document.getElementById("err_mess").innerText = "";
    return 1
    }
}

function validateifcc() {
    var ifcc_value = parseFloat(document.getElementById("ifcc").value);
    ifcc_lower = ((2.5 - 2.15) * 10.929).toFixed(2);
    ifcc_upper = ((24 - 2.15) * 10.929).toFixed(2);
    if (isNaN(ifcc_value) || ifcc_value < ifcc_lower || ifcc_value > ifcc_upper) {
    document.getElementById("ifcc").value = "";
    document.getElementById("err_mess").innerText = "Enter a value between " + ifcc_lower + " and "+ ifcc_upper + " for IFCC";
    document.getElementById("dcct").value = "";
    document.getElementById("mg_dl").value = "";
    document.getElementById("mmol_l").value = "";
    return 0
    } else {
    document.getElementById("err_mess").innerText = "";
    return 1
    }
}

function validate_mg_dl() {
    var mg_dl_value = parseFloat(document.getElementById("mg_dl").value);
    mg_dl_lower = ((2.5 * 28.7) - 46.7).toFixed(2);
    mg_dl_upper = ((24 * 28.7) - 46.7).toFixed(2);
    if (isNaN(mg_dl_value) || mg_dl_value < mg_dl_lower ||mg_dl_value > mg_dl_upper) {
    document.getElementById("dcct").value = "";
    document.getElementById("err_mess").innerText = "Enter a value between " + mg_dl_lower +" and " + mg_dl_upper + " for mg/dl";
    document.getElementById("ifcc").value = "";
    document.getElementById("mg_dl").value = "";
    document.getElementById("mmol_l").value = "";
    return 0
    } else {
    document.getElementById("err_mess").innerText = "";
    return 1
    }
}

function validate_mmol_l() {
    var mmol_l_value = parseFloat(document.getElementById("mmol_l").value);
    mmol_l_lower = ((2.5 * 1.59) - 2.04).toFixed(2);
    mmol_l_upper = ((24 * 1.59) - 2.04).toFixed(2);
    if (isNaN(mmol_l_value) || mmol_l_value < mmol_l_lower ||mmol_l_value > mmol_l_upper) {
    document.getElementById("dcct").value = "";
    document.getElementById("err_mess").innerText = "Enter a value between " + mmol_l_lower +" and " + mmol_l_upper + " for mmol/l";
    document.getElementById("ifcc").value = "";
    document.getElementById("mg_dl").value = "";
    document.getElementById("mmol_l").value = "";
    return 0
    } else {
    document.getElementById("err_mess").innerText = "";
    return 1
    }
}
</script>
