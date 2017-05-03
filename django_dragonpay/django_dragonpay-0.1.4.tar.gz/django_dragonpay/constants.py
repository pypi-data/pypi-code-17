# Dragonpay status codes
# See Appendix 3 of Dragonpay API documentation
DRAGONPAY_STATUS_CODES = {
    'S': 'Success',
    'F': 'Failed',
    'P': 'Pending',
    'U': 'Unknown',
    'R': 'Refund',
    'K': 'Chargeback',
    'V': 'Voided',
    'A': 'Authorized',
    'G': 'In progress',
}

# Dragonpay error codes.
# See Appendix 2 of Dragonpay API documentation
DRAGONPAY_ERROR_CODES = {
    '000': 'Success',
    '101': 'Invalid payment gateway id',
    '102': 'Incorrect secret key',
    '103': 'Invalid reference number',
    '104': 'Unauthorized access',
    '105': 'Invalid token',
    '106': 'Currency not supported',
    '107': 'Transaction cancelled',
    '108': 'Insufficient funds',
    '109': 'Transaction limit exceeded',
    '110': 'Error in operation',
    '111': 'Invalid parameters',
    '201': 'Invalid Merchant Id',
    '202': 'Invalid Merchant Password'
}


DRAGONPAY_PAYOUT_ERROR_CODES = {
    '0': 'Successfully created payout request',
    '-1': 'Invalid credentials or apiKey',
    '-2': '(reserved)',
    '-3': '(reserved)',
    '-4': 'Unable to create payout transaction (internal error)',
    '-5': 'Invalid account no / details',
    '-6': 'Invalid pre-dated run date',
    '-7': 'Amount exceeds limit for payout channel',
    '-8': 'A payout has been previously requested for the same merchant txn id'
}

# Dragonpay Paymemnt method FILTERS
ONLINE_BANKING = 1       # Online banking
OTC_BANK = 2             # Over-the-Counter Banking and ATM
OTC_NON_BANK = 4         # Over-the-Counter non-Bank
# 8 (unused)
# 16 (reserved internally)
PAYPAL = 32              # PayPal
CREDIT_CARDS = 64        # Credit Cards
MOBILE = 128             # Mobile (Gcash)
INTERNATIONAL_OTC = 256  # International OTC
