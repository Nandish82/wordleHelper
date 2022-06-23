const manipdom={

    createKeyBoard : function(){
        // create container for keyboard
        const keyboard_container=document.createElement("div");
        keyboard_container.setAttribute("id","key-container");
        keyboard_container.setAttribute("class","keyboard-container");
        document.body.appendChild(keyboard_container); //add element to body
        var t=document.getElementById("key-container");
        var keyboardLetter=[['Q','W','E','R','T','Y','U','I','O','P'],
                              ['A','S','D','F','G','H','J','K','L'],
                              ['Enter','Z','X','C','V','B','N','M','BackSpace']];
        var classNames=["key-container-row-1","key-container-row-2","key-container-row-3"]
      
            for(let i=0;i<classNames.length;i++){
            var cElem=document.createElement("div")
            cElem.setAttribute("class",classNames[i])
            cElem.setAttribute("id","keys-row-"+(i+1))
            for(let j=0;j<keyboardLetter[i].length;j++){
                var idStr="key-"+keyboardLetter[i][j];
                var p=document.createElement("button");
                var id=document.createAttribute("id");
                p.innerHTML=keyboardLetter[i][j];
                p.setAttribute("class","key")
                p.setAttribute("id",idStr);
                p.setAttribute("onclick","VirtualKeyboardClick(event)")
                if (keyboardLetter[i][j]==='Enter'){
                 p.setAttribute("class","key Enter")
             }
                if(keyboardLetter[i][j]==='BackSpace')
                {
                p.setAttribute("class","key BackSpace")
                p.innerHTML="";
                }
            
            
                cElem.appendChild(p);
            }
            t.appendChild(cElem);
        }
    },
    removeKeyBoard : function (){
        var r=document.getElementById("key-container");
        document.body.removeChild(r);
    },
    createWordleGrid : function(){
        const outer_container=document.createElement("div");
        outer_container.setAttribute("class","outer-container");
        // the outer container contains three div element
        const empty=document.createElement("div");
        const grid=document.createElement("div");
        const status=document.createElement("div");

        grid.setAttribute("id","grid-container");
        grid.setAttribute("class","rel");

        status.setAttribute("id","status-container");
        status.setAttribute("class","status-container");

        outer_container.appendChild(empty);
        outer_container.appendChild(grid);
        outer_container.appendChild(status);

        document.body.appendChild(outer_container);
        // create wordle grid squares
        var t=document.getElementById("grid-container");
        for(let i=0;i<6;i++){
          for(let j=0;j<5;j++)
        {
          var idStr="row-"+i+"col-"+j;
          var p=document.createElement("div");
          var id=document.createAttribute("id");
        
          p.setAttribute("id",idStr);
          p.setAttribute("class","input")
          p.setAttribute("name",idStr);
          p.setAttribute("onclick","squareClick(event)")
          p.setAttribute("style","background-color : #ffffff")
          t.appendChild(p);
        
          var height=calcHeight(idStr);
          document.getElementById(idStr).style.height=height;
        }
        }
        document.getElementById("row-0col-0").setAttribute("class","current-input"); //set initial input
        // create the status rectangle 
        var t=document.getElementById("status-container");
        for(let i=0;i<6;i++){
            var idStr="status-row-"+i
            var p=document.createElement("span");
            p.setAttribute("class","status-row");
            p.setAttribute("id",idStr);
            t.appendChild(p);
            }
        },
    
    createAnalysisOuter : function (){
        // creates the outer structure to display the analysis
        // it contains the header
        const analysis_frame=document.createElement("div");
        analysis_frame.setAttribute("class","analyse-frame");
        analysis_frame.setAttribute("id","analyse-frame");

        // header format: [EMPTY]  SKILL  LUCK  SOLUTIONS REMAINING
        /* 
        <div class="analyse-top-container">
            <div class="analyse-wordle-container"></div>
            <div class="wordle-grade" style="color:#0088FF">SKILL</div>
            <div class="wordle-grade" style="color:#0088FF">LUCK</div>
            <div class="wordle-soln-rem" style="color:#0088FF">SOLUTION <br> REMAINING</div>
        </div>
        */

        const top_container=document.createElement("div");
        top_container.setAttribute("class","analyse-top-container");
        
        const wordle_container=document.createElement("div"); //is empty in header
        wordle_container.setAttribute("class","analyse-wordle-container");

        const skill_dom=document.createElement("div");
        skill_dom.setAttribute("class","wordle-grade-header");
        skill_dom.innerHTML="SKILL";

        const luck_dom=document.createElement("div");
        luck_dom.setAttribute("class","wordle-grade-header");
        luck_dom.innerHTML="LUCK";

        const sln_dom=document.createElement("div");
        sln_dom.setAttribute("class","wordle-soln-rem");
        sln_dom.innerHTML="Solution <br> Remaining";

        top_container.appendChild(wordle_container);
        top_container.appendChild(skill_dom);
        top_container.appendChild(luck_dom);
        top_container.appendChild(sln_dom);

        analysis_frame.appendChild(top_container);
        document.body.appendChild(analysis_frame);




    },
   
    createRowAnalysis : function (word="PAUSE", clue="xxxgy", skill="90", luck="30", soln="4",colorDef={
    "w" : "#ffffff","y" : "#e6b800", "g" : "#39ac39", "x" : "#808080" } ){
        /*
        <div class="analyse-top-container">
            <div class="analyse-wordle-container">
                <span class="analyse-wordle-elem">P</span>
                <span class="analyse-wordle-elem">A</span>
                <span class="analyse-wordle-elem">U</span>
                <span class="analyse-wordle-elem">S</span>
                <span class="analyse-wordle-elem">E</span>
            </div>
            <div class="wordle-grade">90</div>
            <div class="wordle-grade">-</div>
            <div class="wordle-grade">3</div>
        </div>
        */

        const top_container=document.createElement("div");
        top_container.setAttribute("class","analyse-top-container");
        
        const wordle_container=document.createElement("div");
        wordle_container.setAttribute("class","analyse-wordle-container");
        for(let i=0;i<word.length;i++)
        {
            var s=document.createElement("span");
            s.setAttribute("class","analyse-wordle-elem");
            s.innerHTML=word[i];
            s.style.backgroundColor=colorDef[clue[i]];
            wordle_container.appendChild(s)
        }

        const skill_dom=document.createElement("div");
        skill_dom.setAttribute("class","wordle-grade");
        skill_dom.innerHTML=skill;

        const luck_dom=document.createElement("div");
        luck_dom.setAttribute("class","wordle-grade");
        luck_dom.innerHTML=luck;

        const sln_dom=document.createElement("div");
        sln_dom.setAttribute("class","wordle-grade");
        sln_dom.innerHTML=soln;

        top_container.appendChild(wordle_container);
        top_container.appendChild(skill_dom);
        top_container.appendChild(luck_dom);
        top_container.appendChild(sln_dom);

        var analysis_frame=document.getElementById("analyse-frame")
        analysis_frame.appendChild(top_container);
    }

    
    

}