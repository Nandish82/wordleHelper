class Wordle {

    constructor()
    {
          this.word_list=['gully', 'saner', 'budge', 'arson', 'crass', 'smash', 'amaze', 'rerun', 'slyly', 'sieve', 'peril', 'stunt', 'pansy', 'depth', 'seedy', 'glide', 'glide', 'diver', 'rupee', 'heave', 'inert', 'basal', 'fetch', 'aglow', 'queue']
    }
  
    getClue(attemptword="hello",goalword="slate")
    {
      /* function that returns the clue given a goalword and an attempt word
    x- letter is not in the word
    g- letter is in word and at correct place
    y- letter is in word but not at correct place
    */
          var clue=[ 'x','x','x','x','x']
  
          for(let i=0;i<attemptword.length;i++)
          {
              if (attemptword[i]==goalword[i])
                clue[i]="g"
  
              if (clue[i]!='g')
              {
                for (let j=0;j<goalword.length;j++)
                {
                  if (attemptword[i]==goalword[j])
                    clue[i]="y"
                }
              }
          }
  
    return clue
    }
  
  
    checkWord(wordtocheck,clue,clueword)
    {
      /* given a wordtocheck, the clue and the clue list
         we check if it is a valid word */
  
      var result=[false,false,false,false,false]
  
      for (let c=0;c<clue.length;c++)
      {
        if(clue[c]=='g') //check for g
        {
          if (wordtocheck[c]==clueword[c])
            result[c]=true
        }
  
        else if (clue[c]=='y')  //check for y
        {
          for(let j=0;j<wordtocheck.length;j++)
          {
            if(wordtocheck[j]==clueword[c]) // if same letter in both both words and clue is 'y' that word becomes in valid
              if(c==j)
                {
                  result[c]=false
                  break
                }
              else
              {
                result[c]=true
              }
          }
  
  
        }
        else
        {
          var is_letter_present=true
          for(let j=0;j<wordtocheck.length;j++)
          {
            if(wordtocheck[j]==clueword[c]){
              is_letter_present=true //the letter is present in the word,m so we break here
              break
            }
            else
            {
              is_letter_present=false
            }
          }
  
          if(is_letter_present){
            for(let k=0;k<clueword.length;k++)
            {
              if((clueword[c]==clueword[k]) && (k!=c)){
                if(clue[k]=='g' || clue[k]=='y'){
                  result[c]=true
                  break
                }
              }
            }
          }
          else
          {
            result[c]=true
          }
  
        }
        if(result[c]==false)
          return false
  
      }
      return true
    } //end of checkword function
  } //end of class
  
  function getOriginalList() {
  
    word_list=['gully', 'saner', 'budge', 'arson', 'crass', 'smash', 'amaze', 'rerun', 'slyly', 'sieve', 'peril', 'stunt', 'pansy', 'depth', 'seedy', 'glide', 'glide', 'diver', 'rupee', 'heave', 'inert', 'basal', 'fetch', 'aglow', 'queue']
  
    var sheet = SpreadsheetApp.getActiveSheet();
    var data = sheet.getRange(2,1)
  }
  
  
  
  function Test()
  {
    const wordle1=new Wordle()
    console.log(wordle1.word_list)
    console.log(wordle1.getClue())
  
    console.log(wordle1.checkWord("glade","ygxxx","album"))
  }
  