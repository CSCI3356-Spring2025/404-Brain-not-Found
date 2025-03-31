document.addEventListener('DOMContentLoaded', function() {
    console.log("questions.js file loaded successfully");

    const questionsContainer = document.getElementById("questions-container");
    const addButton = document.getElementById("add-question");

    let totalFormsInput = document.querySelector('input[name="questions-TOTAL_FORMS"]');

    addButton.addEventListener('click', function() {
        let formCount = parseInt(totalFormsInput.value);
        console.log('Adding question number:', formCount);

        const questionDiv = document.createElement('div');
        questionDiv.classList.add('question');

        // Question Text input
        const questionText = document.createElement('input');
        questionText.type = 'text';
        questionText.name = `questions-${formCount}-text`;
        questionText.placeholder = `Question ${formCount + 1}`;
        questionDiv.appendChild(questionText);

        // Question Type select
        const questionType = document.createElement('select');
        questionType.name = `questions-${formCount}-question_type`;

        const optionLikert = document.createElement('option');
        optionLikert.value = 'likert';
        optionLikert.textContent = "Likert Scale";

        const optionOpen = document.createElement('option');
        optionOpen.value = 'open';
        optionOpen.textContent = "Open-Ended";

        questionType.appendChild(optionLikert);
        questionType.appendChild(optionOpen);
        questionDiv.appendChild(questionType);

        // Remove button
        const removeButton = document.createElement('button');
        removeButton.type = 'button';
        removeButton.textContent = 'Remove Question';
        removeButton.addEventListener('click', function() {
            questionDiv.remove();
            console.log('Question removed. Note: TOTAL_FORMS will not decrease dynamically.');
        });
        questionDiv.appendChild(removeButton);

        questionsContainer.appendChild(questionDiv);

        // Update TOTAL_FORMS
        totalFormsInput.value = formCount + 1;
    });
});

// // // static/PeerConnect/js/questions.js

// // document.addEventListener('DOMContentLoaded', function() {
// //     console.log("questions.js file loaded successfully");
    
// //     let questionCount = 0;

// //     const questionsContainer = document.getElementById("questions-container");

// //         //function to create a new question
// //     function createQuestion() {
// //         questionCount+=1;
// //         console.log('in createQuestion function, current count:', questionCount);
        
// //         //DIV
// //         const questionDiv = document.createElement('div');
// //         questionDiv.classList.add('question');
// //         console.log('created new questionDiv:', questionDiv);

// //             // Question - Text Input element
// //         const questionTextInput = document.createElement('input');
// //         questionTextInput.type = 'text';
// //         questionTextInput.name = `question_${questionCount}_text`;
// //         questionTextInput.placeholder = `Question ${questionCount}`;
// //         questionDiv.appendChild(questionTextInput);


// //             // Type - select element
// //         const questionTypeSelect = document.createElement('select');
// //         questionTypeSelect.name = `question_${questionCount}_type`;
// //         console.log('created questionTypeSelect:', questionTypeSelect);

// //             //Options
// //         const optionLikert = document.createElement('option');
// //         optionLikert.value = 'likert';
// //         optionLikert.textContent = "Likert Scale";
// //         questionTypeSelect.appendChild(optionLikert); //add likert to select element
// //         console.log('Added Likert option:', optionLikert);

// //         const optionOpen = document.createElement('option');
// //         optionOpen.value = 'open';
// //         optionOpen.textContent = "Open-Ended";
// //         questionTypeSelect.appendChild(optionOpen); //add likert to select element
// //         console.log('Added Open-Ended option:', optionLikert);

// //         //Append select
// //         questionDiv.appendChild(questionTypeSelect);
        
        
// //         // Creates Remove Question button
// //         const removeButton = document.createElement('button');
// //         removeButton.textContent = "Remove Question";
// //         removeButton.type = 'button';
// //         removeButton.classList.add('remove-question');  // Optionally add a class for styling
// //         removeButton.addEventListener('click', function() {
// //             questionDiv.remove();  // Remove the question div
// //             questionCount-=1;
// //             document.getElementById("num_questions").value = questionCount; //updates num_question
// //             console.log(`Question ${questionCount} removed.`);
// //         });
// //             //append remove
// //         questionDiv.appendChild(removeButton);

// //         //Append div
// //         questionsContainer.appendChild(questionDiv);
// //         console.log('Appended div to container:', questionDiv);
    

// //         document.getElementById("num_questions").value = questionCount;
// //     }

// //         //button to implement createQuestionField
// //     document.getElementById("add-question").addEventListener('click', function() {
// //         console.log('Add question clicked');
// //         createQuestion();
    
// //     });
// // });
