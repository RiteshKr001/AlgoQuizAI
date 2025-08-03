import React, {useEffect, useState } from 'react'
import './App.css'

function GenerateButton({ onClick }) {
  return (
    <button className='gnrt-btn' onClick={onClick}>Generate New Question</button>
  )
}


function Challenge({Challenge_data, ansIndex, setAnsIndex}){
  if (!Challenge_data) {
    return <div>Loading...</div>
  }

  const handleOptionClick = (index) => {
    setAnsIndex(index)
  }

  const options = Challenge_data.options

  const Optns = options.map((op, index) =>
    <div key={index}><button className='optn-cntnr' onClick={() => handleOptionClick(index)}>{op}</button></div>
  );


  return (
    <div>
      <div className='que-cntnr'>{Challenge_data.title}</div>

      <div>{Optns}</div>

      {ansIndex !== null && (
        <div className='ans-cntnr'>
          {ansIndex === Challenge_data.correct_answer_id ? (
            <span className='correct'>Correct Answer!</span>
          ) : (
            <span className='incorrect'>Incorrect Answer! The correct answer is: {Challenge_data.options[Challenge_data.correct_answer_id]}</span>
          )}
          <div>Explanation: <p>{Challenge_data.explanation}</p></div>
        </div>
      )}
    </div>
  )
}



export default function App() {
  const [challengeData, setChallengeData] = useState(null)
  const [ansIndex, setAnsIndex] = useState(null) 
  const fetchChallenge = async () => {
    try {
      const response = await fetch('http://localhost:8000/generate-challenge')
      const data = await response.json()
      setChallengeData(data)
      setAnsIndex(null)
    } catch (error) {
      console.error("Failed to fetch challenge:", error)
    }
  }

  useEffect(() => {
    fetchChallenge()
  }, [])

  return (
    <div className='cntnr'>
      <h2 className='h2-app'>Challenge</h2>
      <Challenge Challenge_data={challengeData} ansIndex={ansIndex} setAnsIndex={setAnsIndex} />
      <GenerateButton onClick={fetchChallenge} />
      <div className='footer'>Made with ❤️ by <a href='https://github.com/RiteshKr001'>Ritesh</a></div>
    </div>
  )
}