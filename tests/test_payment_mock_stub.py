import unittest
from unittest.mock import Mock
from unittest.mock import patch
from CISC_327_CS.services import payment_service
from CISC_327_CS.services import library_service
from CISC_327_CS.services.payment_service import PaymentGateway


# TODO make pyinit file (ask bree)
class test_pay_late_fees(unittest.TestCase):
    def test_successful_payment(self):
        # mock the gateway return values
        gateway_mock = Mock(spec=PaymentGateway)
        patch('services.library_service.get_book_by_id', return_value={'id': 1, 'title': 'test'})
        patch('services.library_services.calculate_late_fee_for_book', return_value={'fee_amount':3.00, 'days_overdue':3, 'status':'success'})

        gateway_mock.process_payment.return_value = (True, "txn_123456", "Late fees for test")
        result = library_service.pay_late_fees('123456', 1, gateway_mock)
        assert result == (True, "txn_123456", "Payment successful! Late fees for test")
        gateway_mock.assert_called_once()

    def test_payment_declined_by_gateway(self):
        gateway_mock = Mock(spec=PaymentGateway)

        patch('services.library_service.get_book_by_id', return_value={'id': 1, 'title': 'test'})
        patch('services.library_services.calculate_late_fee_for_book', return_value={'fee_amount':3.00, 'days_overdue':3, 'status':'success'})
        gateway_mock.process_payment.return_value = (False, None, "Payment declined")
        result = library_service.pay_late_fees('123456', 1, gateway_mock)
        assert result == (False, "txn_123456", "Payment failed: Payment declined")
    
    def invalid_patron_ID(self):
        gateway_mock = Mock(spec=PaymentGateway)

        result = library_service.pay_late_fees('12345', 1)
        assert result == (False, "Invalid patron ID. Must be exactly 6 digits.", None)
        gateway_mock.assert_not_called()
        
    def zero_late_fees(self):
        gateway_mock = Mock(spec=PaymentGateway)

        patch('services.library_service.get_book_by_id', return_value={'id': 1, 'title': 'test'})
        patch('services.library_services.calculate_late_fee_for_book', return_value={'fee_amount':0.00, 'days_overdue':0, 'status':'success'})
        result = library_service.pay_late_fees('123456', 1)
        assert result == (False, "No late fees to pay for this book.", None)
        gateway_mock.assert_not_called()

    def network_error_handling_exception(self):
        gateway_mock = Mock(spec=PaymentGateway)

        gateway_mock.process_payment.return_value = (False, "txn_123456", "Gateway Error")
        result = library_service.pay_late_fees('123456', 1, gateway_mock)
        assert result == ("Payment processing error: Gateway Error")
        gateway_mock.assert_called_once()

class test_refund_late_fee_payment(unittest.TestCase):
    def test_successful_refund(self):
        gateway_mock = Mock(spec=PaymentGateway)

        gateway_mock.refund_payment.return_value = (True, "txn_123456", f"Refund late fees for test")
        result = library_service.refund_late_fee_payment('123456', 1, gateway_mock)
        assert result == (True, "txn_123456", f"Payment successful! Late fees for test")
        gateway_mock.assert_called_once()

