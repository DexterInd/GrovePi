function round(number, precision) {
    if (isNaN(number)) return NOT_AVAILABLE
    if (precision == undefined || isNaN(precision))
        precision = 2
    var factor = Math.pow(10, precision)
    var tempNumber = number * factor
    var roundedTempNumber = Math.round(tempNumber)
    return roundedTempNumber / factor
}

const NOT_AVAILABLE = 'N/A'

module.exports = {
    round,
    NOT_AVAILABLE
}