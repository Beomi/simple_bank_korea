var apiUrl = 'https://2ok33s4416.execute-api.ap-northeast-2.amazonaws.com/api/kb'

document.addEventListener('DOMContentLoaded', function (e) {
    var form = document.querySelector('form')
    var submitButton = document.querySelector('#submitButton')
    var resultBox = document.querySelector('#resultBox')
    form.addEventListener('submit', function (e) {
        e.preventDefault()
        submitButton.classList.add('disabled')
        submitButton.innerText = 'Querying...'
        axios.post(apiUrl, {
            "BANK_ACCOUNT_NO": form.bank_num.value,
            "BIRTHDAY": form.birthday.value,
            "PASSWORD": form.password.value
        }).then(function (res) {
            if (res.data.error) {
                alert(res.data.error)
                break;
            }
            return res.data
        }).then(function (valueList) {
            //{date: "2018-03-01T12:59:13", amount: -23500, balance: 951156, transaction_by: "N_롯데쇼핑("}
            submitButton.classList.remove('disabled')
            submitButton.innerText = 'Query!'
            var html = ''
            valueList.forEach(function (value) {
                var _date = '<td>' + value.date + '</td>'
                var _amount = '<td>' + value.amount + '</td>'
                var _balance = '<td>' + value.balance + '</td>'
                var _transaction_by = '<td>' + value.transaction_by + '</td>'
                var _row = _date + _amount + _balance + _transaction_by
                html += '<tr>' + _row + '</tr>'
            })
            return html
        }).then(function (html) {
            resultBox.innerHTML = html
        })
    })
})
