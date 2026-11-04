class LoanRepository:
    _loans = []
    _next_id = 1

    @classmethod
    def create(cls, data):
        loan = {
            "id": cls._next_id,
            "valor": float(data.get("valor", 0)),
            "months": int(data.get("months", 12)),
            "monthly_installment": float(data.get("monthly_installment", 0)),
            "total_payable": float(data.get("total_payable", 0))
        }
        cls._loans.append(loan)
        cls._next_id += 1
        return loan

    @classmethod
    def list_all(cls):
        return cls._loans

    @classmethod
    def find_by_id(cls, loan_id):
        return next((loan for loan in cls._loans if loan['id'] == loan_id), None)

    @classmethod
    def update(cls, loan_id, new_data):
        loan = cls.find_by_id(loan_id)
        if loan:
            if "valor" in new_data: loan["valor"] = float(new_data["valor"])
            if "months" in new_data: loan["months"] = int(new_data["months"])
            if "monthly_installment" in new_data: loan["monthly_installment"] = float(new_data["monthly_installment"])
            if "total_payable" in new_data: loan["total_payable"] = float(new_data["total_payable"])
            return loan
        return None

    @classmethod
    def delete(cls, loan_id):
        loan = cls.find_by_id(loan_id)
        if loan:
            cls._loans.remove(loan)
            return True
        return False