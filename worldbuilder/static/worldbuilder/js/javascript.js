function setDice() {
    var diceRolls = document.querySelectorAll("span.diceRoll");
    diceRolls.forEach(function(element) {
        element.addEventListener("click", rollDice);
    });
}

function rollDice(event) {
    var diceText = event.target.innerHTML.split('d');
    var numDice = parseInt(diceText[0],10);
    var diceSize = parseInt(diceText[1],10);
    var rollResult = 0;
    for( var i = numDice; i > 0; i--) {
        rollResult += Math.floor(Math.random() * diceSize) + 1;
    }
    event.target.innerHTML = event.target.innerHTML.split(' ')[0] + ' = ' + rollResult.toString();
}