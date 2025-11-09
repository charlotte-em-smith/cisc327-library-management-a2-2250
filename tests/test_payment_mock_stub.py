import unittest
from unittest.mock import Mock
from unittest.mock import patch
from CISC_327_CS.services import payment_service
from CISC_327_CS.services import library_service
from CISC_327_CS.services.payment_service import PaymentGateway


# TODO make pyinit file (ask bree)
class TestPayLateFees():
    def test_successful_payment(self, mocker):
        # mock the gateway return values
        gateway_mock = Mock(spec=PaymentGateway)
        mocker.patch('CISC_327_CS.services.library_service.get_book_by_id', return_value={'id': 1, 'title': 'test'})
        mocker.patch('CISC_327_CS.services.library_service.calculate_late_fee_for_book', return_value={'fee_amount':3.00, 'days_overdue':3, 'status':'success'})

        gateway_mock.process_payment.return_value = (True, "txn_123456", "Late fees for test")
        result = library_service.pay_late_fees('123456', 1, gateway_mock)
        assert result == (True, "Payment successful! Late fees for test", "txn_123456")

        gateway_mock.process_payment.assert_called_once()

    def test_payment_declined_by_gateway(self, mocker):
        gateway_mock = Mock(spec=PaymentGateway)

        mocker.patch('CISC_327_CS.services.library_service.get_book_by_id', return_value={'id': 1, 'title': 'test'})
        mocker.patch('CISC_327_CS.services.library_service.calculate_late_fee_for_book', return_value={'fee_amount':3.00, 'days_overdue':3, 'status':'success'})

        gateway_mock.process_payment.return_value = (False, None, "Payment declined")
        result = library_service.pay_late_fees('123456', 1, gateway_mock)
        assert result == (False, "Payment failed: Payment declined", None)

        gateway_mock.process_payment.assert_called_once()
    
    def test_invalid_patron_ID(self):
        gateway_mock = Mock(spec=PaymentGateway)

        result = library_service.pay_late_fees('12345', 1)
        assert result == (False, "Invalid patron ID. Must be exactly 6 digits.", None)

        gateway_mock.assert_not_called()
        
    def test_zero_late_fees(self, mocker):
        gateway_mock = Mock(spec=PaymentGateway)

        mocker.patch('CISC_327_CS.services.library_service.get_book_by_id', return_value={'id': 1, 'title': 'test'})
        mocker.patch('CISC_327_CS.services.library_service.calculate_late_fee_for_book', return_value={'fee_amount':0.00, 'days_overdue':0, 'status':'success'})
        
        result = library_service.pay_late_fees('123456', 1)
        assert result == (False, "No late fees to pay for this book.", None)

        gateway_mock.assert_not_called()

    def test_network_error_handling_exception(self, mocker):
        gateway_mock = Mock(spec=PaymentGateway)

        mocker.patch('CISC_327_CS.services.library_service.get_book_by_id', return_value={'id': 1, 'title': 'test'})
        mocker.patch('CISC_327_CS.services.library_service.calculate_late_fee_for_book', return_value={'fee_amount':3.00, 'days_overdue':3, 'status':'success'})

        gateway_mock.process_payment.return_value = (False, "txn_123456", "Payment processing error: Gateway Error")
        result = library_service.pay_late_fees('123456', 1, gateway_mock)
        assert result == (False, "Payment failed: Payment processing error: Gateway Error", None)

        gateway_mock.process_payment.assert_called_once()

class TestRefundLateFeePayment():
    def test_successful_refund(self):
        gateway_mock = Mock(spec=PaymentGateway)

        gateway_mock.refund_payment.return_value = (True, "Refund of $2.00 processed successfully. Refund ID: txn_123456")
        success, msg = library_service.refund_late_fee_payment('txn_123456', 2.00, gateway_mock)
        assert msg == "Refund of $2.00 processed successfully. Refund ID: txn_123456"
        assert success == True

        gateway_mock.refund_payment.assert_called_once()

    def test_invalid_transaction_ID_rejection(self):
        gateway_mock = Mock(spec=PaymentGateway)

        success, msg = library_service.refund_late_fee_payment('123456', 2.00)
        assert msg == "Invalid transaction ID."
        assert success == False

        gateway_mock.refund_payment.assert_not_called()

    def test_invalid_refund_amount_neg(self):
        gateway_mock = Mock(spec=PaymentGateway)

        success, msg = library_service.refund_late_fee_payment('txn_123456', -1.00)
        assert msg == "Refund amount must be greater than 0."
        assert success == False

        gateway_mock.refund_payment.assert_not_called()

    def test_invalid_refund_amount_zero(self):
        gateway_mock = Mock(spec=PaymentGateway)

        success, msg = library_service.refund_late_fee_payment('txn_123456', 0.00)
        assert msg == "Refund amount must be greater than 0."
        assert success == False

        gateway_mock.refund_payment.assert_not_called()
    
    def test_invalid_refund_amount_max(self):
        gateway_mock = Mock(spec=PaymentGateway)

        success, msg = library_service.refund_late_fee_payment('txn_123456', 16.00)
        assert msg == "Refund amount exceeds maximum late fee."
        assert success == False

        gateway_mock.refund_payment.assert_not_called()

