const solve={
    getListWords : function (){ //returns the wordle list
        var word_list=getWords().map(function(r){ return atob(r)});
        return word_list;
    },

    checkWord : function(wordtocheck,clue,clueword){ //return true if wordtocheck is valid according to the clues
        /*  given a word (wordtocheck), a clue, the word used to 
            get that clue (clueword), this function returns if 
            that word is valid
            e.g wordtocheck= PAUSE, clue=XGXYX, clueword=FARCE
            the function should return false since the A
            is in correct place in PAUSE but there is no 
            'C'in PAUSE.
        */

    }
}