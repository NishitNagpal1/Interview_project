import React,{ useState,useEffect } from "react";
import { getQuestions,submitAnswer } from "./apifrontend";
import "../styles/Quiz.css";


const Quiz=() => {
    const [questions,setQuestions] = useState([]);
    const [currentQuestionIndex,setCurrentQuestionIndex] =useState(0);
    const [selectedOption,setSelectedOption] =useState(null);
    const [isLoading,setIsLoading] =useState(true);

    useEffect(() => {
        const fetchQuestions =async() =>{
            try {
                const data = await getQuestions(10);
                setQuestions =data;
                setIsLoading=false;
            } catch(error){
                console.error("Error fetching questions:",error);
            }
            };
            fetchQuestions();
        }, []);
    

const handleOptionChange =(option) =>{
    setSelectedOption(option);
};


const handleSubmit =async () => {
   if  (selectedOption==null){
    alert("Please Select some option!");
    return
   }
   try {
    const result =await submitAnswer({
        question_id:questions[currentQuestionIndex].id,
        selected_option: selectedOption,
    });
    alert(result.message);
   } catch(error){
    console.error("Error submitting answer:",error);
   }
   setSelectedOption(null);
   setCurrentQuestionIndex((prev)=>prev +1);
};


if (isLoading){
    return <div>Loading Questions...Please Wait</div>;
}

if (currentQuestionIndex >= questions.lenght){
    return <div> You have Completed the quiz!!</div>;
}

const currentQuestion =questions[currentQuestionIndex];

return (
    <div className ="quiz-container">
       <div className="question-box">{currentQuestion.text}</div>
        <div className="options-box">
            {currentQuestion.options.map((option,index)=>(
                <label key={index}>
                    <input
                    type="radio"
                    name="option"
                    value={option}
                    checked={selectedOption===option}
                    onChange={() => handleOptionChange(option)}
                    />
                    {option}
                </label>
            ))}
        </div>
        <button 
        onClick={handleSubmit}
        disabled={selectedOption === null}
        > Submit 
        </button>
        </div>
);
};