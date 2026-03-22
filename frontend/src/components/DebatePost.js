import { useRouter } from "next/router";
import { useState, useEffect } from "react";
import Comment from "./Comment";

const PUBLIC_IP = "54.80.13.110";

function DebatePost({ loadingUser, isLoggedIn }) {
  const router = useRouter(); // passing in all the debate information in the router.
  const {
    debateId,
    username,
    currentUser,
    title,
    created_at,
    content,
    percentage,
    userProfilePic,
    numberComments,
    currentProfilePic,
  } = router.query;

  const [showReplyForm, setShowReplyForm] = useState(false); // State for showing the reply form when making a comment
  const [replyContent, setReplyContent] = useState(""); // Reply content state
  const [parentCommentId, setParentCommentId] = useState(null); // Track parent comment
  const [comments, setComments] = useState([]); // Store fetched comments
  const [summary, setSummary] = useState(""); // Stores summary
  const [sliderValue, setSliderValue] = useState(50); // Initial slider value
  const [averagePercentage, setAveragePercentage] = useState(0); // stores average percent

  // This function is responsible for gathering the percentage the user gave
  const fetchUserPercentage = async () => {
    try {
      const response = await fetch(
        `http://${PUBLIC_IP}/api/get_percentage/?debateId=${debateId}&user=${currentUser}`
      );
      if (response.ok) {
        const data = await response.json();
        if (data.percentage !== undefined) {
          setSliderValue(data.percentage); // setting slider value to percentage the user gave
        } else {
          setSliderValue(50); // back to default if error occurs
        }
      } else {
        setSliderValue(50);
      }
    } catch (error) {
      console.error("Error fetching user percentage:", error);
      setSliderValue(50); // back to default if error occurs
    }
  };

  // This function is responsible for gathering all the comments relating to that debate
  const fetchComments = async () => {
    try {
      const response = await fetch(
        `http://${PUBLIC_IP}/api/comments?debateId=${debateId}`
      );
      if (response.ok) {
        const data = await response.json();
        setComments(data); // Update the state with fetched comments
      } else {
        console.error("Failed to fetch comments");
      }
    } catch (error) {
      console.error("Error fetching comments:", error);
    }
  };

  // This function is responsible for fetching the average percent for that debate
  const fetchAveragePercentage = async () => {
    try {
      const response = await fetch(
        `http://${PUBLIC_IP}/api/average_percentage/${debateId}/`
      );
      if (response.ok) {
        const data = await response.json();
        setAveragePercentage(data.average_percentage); // setting the average percentage state to what was returned
      } else {
        console.error("Failed to fetch average percentage");
      }
    } catch (error) {
      console.error("Error fetching average percentage:", error);
    }
  };

  useEffect(() => {
    if (debateId && username) {
      // calling all fetching functions
      fetchUserPercentage();
      fetchComments();
      fetchAveragePercentage();
    }
  }, [debateId, username]);

  // Opening the comment text box
  const handleReplyClick = (commentId = null) => {
    // commentId will be null if its replying to a debate.
    setParentCommentId(commentId); // setting parent comment Id to null.
    setShowReplyForm((prevState) => !prevState); // opening reply form
  };

  const addReply = (newReply) => {
    setComments((prevComments) => [...prevComments, newReply]);
  };

  const getAIComment = async () => {
    try {
      // Send the GET request with the prompt as a query parameter
      const getResponse = await fetch(
        `http://${PUBLIC_IP}/api/get_ai_comment/?content=${encodeURIComponent(
          content
        )}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (getResponse.ok) {
        // Parse the JSON response
        const data = await getResponse.json();
        const botComment = data.bot_comment; // Extract the bot's comment
        const botUser = data.username;

        // Create the replyData for the POST request
        const replyData = {
          parent_debate: debateId,
          parent_comment: parentCommentId,
          content: botComment,
          username: botUser,
        };

        // Send the POST request to submit the bot comment
        const postResponse = await fetch(
          `http://${PUBLIC_IP}/api/comments/`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(replyData), // Send the replyData as JSON
          }
        );

        if (postResponse.ok) {
          fetchComments(); // Refresh comments instantly
        } else {
          console.error("Failed to submit AI reply");
        }
      } else {
        console.error("Failed to get AI comment");
      }
    } catch (error) {
      console.error("Error submitting AI reply:", error);
    }
  };

  // adding comment to backend and displaying it on screen
  const handleReplySubmit = async () => {
    const replyData = {
      parent_debate: debateId,
      parent_comment: parentCommentId,
      content: replyContent,
      username: currentUser,
      profilepicture: currentProfilePic,
    };

    try {
      const response = await fetch(`http://${PUBLIC_IP}/api/comments/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(replyData),
      });

      if (response.ok) {
        setShowReplyForm(false); // closing reply form
        setReplyContent(""); // reseting reply content
        fetchComments(); // fetching the comments to update it instantly.
        getAIComment();
      } else {
        console.error("Failed to submit reply");
      }
    } catch (error) {
      console.error("Error submitting reply:", error);
    }
  };

  // This is responsible for changing the agreement if the user wishes to do so.
  const handleAgreementChange = async (newSliderValue) => {
    try {
      setSliderValue(newSliderValue); // Update the local slider value

      const response = await fetch(
        `http://${PUBLIC_IP}/api/add_percentage/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user: currentUser,
            debateId: debateId,
            percentage: newSliderValue,
          }),
        }
      );

      const contentType = response.headers.get("content-type");

      if (contentType && contentType.indexOf("application/json") !== -1) {
        await response.json();
        fetchAveragePercentage(); // updating the percentage so it updates instantly.
      } else {
        const textResponse = await response.text();
        console.error("Received non-JSON response:", textResponse);
      }
    } catch (error) {
      console.error("Failed to submit percentage:", error.message);
    }
  };

  const handleSummariseClick = async () => {
    setSummary("Generating AI Summary...");
    try {
      const response = await fetch(`http://${PUBLIC_IP}/api/run_llm/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          action: "factcheck",
          input_text: content,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setSummary(data.output);
      } else {
        console.error("Error:", response.statusText);
      }
    } catch (error) {
      console.error("Error summarising:", error);
    }
  };

  return (
    <div className="flex justify-center flex-col items-center overflow-hidden box-border">
      <div className="w-[80%] bg-[#1a0033] mb-5 mt-3 box-border overflow-hidden">
        <div className="flex w-full h-[150px] bg-gray-950 text-white items-center justify-between p-5">
          <div className="flex items-center">
            <img
              className="rounded-full h-[100px] m-5 object-cover"
              src={
                userProfilePic
                  ? `http://${PUBLIC_IP}${userProfilePic}`
                  : "/images/defaultProfilePic.png"
              }
              alt="User Profile"
            />
            <div className="flex flex-col m-3 space-y-3">
              <h1 className="flex flex-col space-y-1">{title}</h1>
              <div className="flex space-x-3">
                <h2>{username}</h2>
                <h2>{new Date(created_at).toLocaleDateString("en-GB")}</h2>
              </div>
            </div>
          </div>
          <div className="border-2 h-10 flex items-center justify-center w-[20%]">
            <p className="m-1">{averagePercentage}%</p>
          </div>

          {!loadingUser && (
            <div className="flex flex-col items-center mt-5">
              <input
                type="range"
                min="0"
                max="100"
                value={sliderValue}
                onChange={(e) => handleAgreementChange(e.target.value)}
                className="w-[80%]"
              />
              <span className="text-white mt-2">
                Your Agreement: {sliderValue}%
              </span>
            </div>
          )}

          <div className="flex space-x-4">
            <div className="custom_button" onClick={handleSummariseClick}>
              Summarise and Fact Check
            </div>
            {!loadingUser && (
              <div
                className="custom_button flex items-center justify-center cursor-pointer"
                onClick={() => handleReplyClick(null)}
              >
                Comment
              </div>
            )}
          </div>
        </div>

        {summary && (
          <div className="flex items-top m-5">
            <h1 className="pt-5">✨</h1>
            <div className="reply_box p-7">
              <textarea
                className="invisible_box w-full"
                readOnly
                value={summary}
                placeholder="Generated Summary..."
                rows={summary.split("\n").length}
              />
            </div>
          </div>
        )}

        <div className="text-white m-5">
          <p>{content}</p>
        </div>

        {showReplyForm && (
          <div className="reply_box">
            <textarea
              className="invisible_box"
              placeholder="Write your reply..."
              value={replyContent}
              onChange={(e) => setReplyContent(e.target.value)}
            />
            <button className="custom_button" onClick={handleReplySubmit}>
              Submit Reply
            </button>
          </div>
        )}
      </div>

      <div className="w-[80%]">
        {/* mapping all the comments */}
        {comments
          .filter((comment) => comment.parent_comment === null)
          .map((comment) => (
            <Comment
              key={comment.comment_id}
              comment={comment}
              comments={comments}
              parentDebateId={debateId}
              loadingUser={loadingUser}
              addReply={addReply}
              currentUser={currentUser}
              currentProfilePic={comment.profile_picture}
            />
          ))}
      </div>
    </div>
  );
}

export default DebatePost;



