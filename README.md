# OpenTax
Free, open-source US tax prep software.

For now, this program is meant to run 100% locally, for print-and-file tax preparation. These might change if this software becomes more widely used but for now I'm focusing on a working proof-of-concept.
  * IRS MeF e-filing requires becoming an Authorized IRS e-file Provider (Pub 3112, pass ATS, EFIN, Pub 1345/4164).
  * No data is received or stored on any server, as this will trigger tax-preparer (PTIN) and FTC Safeguards Rule (GLBA) obligations.

**DISCLAIMER**: I am not a licensed tax preparer. I am doing this for fun.

# User Instructions
## Installation
(TODO)

## Usage
1. Drag and drop your PDFs forms into the [???]
2. The program will parse the PDFs. Make sure to manually review the numbers and edit if necessary!
3. The program will auto-populate your output forms. Make sure to manually review the proposals and edit if necessary!
4. The output forms will be printed as a PDF. Print, sign, and file accordingly.

# LIMITATIONS
We're working on it! Currently this software only supports:
* // INCOMPLETE

On our to-do list:
* Priority 1
  * Federal
    * W2
    * 1099-INT
    * 1040
    * Standard deduction
    * Filing statuses: single, married jointly, married separately / qualifying surviving spouse, HOH
    * Credits: EITC (Schedule EIC + worksheet), CTC/ACTC (Schedule 8812).
* Priority 2
  * Federal
    * schedule A, itemized deductions
    * schedule C
    * schedule D + 8949
    * rental
    * K1
    * AMT
* Priority 3
  * state returns

# Want to contribute?
See [DEVELOPMENT.md](https://github.com/imaqt314/OpenTax/blob/main/DEVELOPMENT.md)
