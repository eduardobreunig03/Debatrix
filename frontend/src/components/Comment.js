import { useState } from "react";
const PUBLIC_IP = "54.80.13.110";

export default function Comment({
  comment,
  comments,
  parentDebateId,
  depth = 0,
  loadingUser,
  addReply, // Accept the function from the parent
  currentUser,
  currentProfilePic,
}) {
  const [showReplyForm, setShowReplyForm] = useState(false);
  const [replyContent, setReplyContent] = useState("");

  // Filter replies for the current comment
  const replies = comments.filter(
    (c) => c.parent_comment === comment.comment_id
  );

  // Handle reply form submission
  const handleReplySubmit = async () => {
    const replyData = {
      parent_debate: parentDebateId,
      parent_comment: comment.comment_id,
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
        const newReply = await response.json(); // Get the new reply from the response
        addReply(newReply); // Add the new reply to the parent component's state
        setShowReplyForm(false);
        setReplyContent("");
      } else {
        console.error("Failed to submit reply");
      }
    } catch (error) {
      console.error("Error submitting reply:", error);
    }
  };

  return (
    <div className="flex flex-col items-center w-full mt-3 relative">
      <div
        className="flex w-full mt-3 relative"
        style={{ paddingLeft: depth > 0 ? `${depth * 50}px` : "0px" }}
      >
        <div className="flex h-[150px] w-full bg-gray-950 text-white items-center relative">
          {depth > 0 && (
            <div className="absolute h-full " style={{ left: `-20px` }}></div>
          )}
          <div className="flex items-center justify-center">
            <img
              className="rounded-full h-16 w-16 m-1 object-cover"
              src={
                comment.profilepicture
                  ? `http://${PUBLIC_IP}${comment.profilepicture}`
                  : "/images/defaultProfilePic.png"
              }
              alt="User Profile"
            />
          </div>
          <div className="flex flex-col m-3 space-y-3">
            <div className="flex flex-col">
              <h2>{comment.username}</h2>
              <h2>{new Date(comment.date).toLocaleDateString("en-GB")}</h2>
            </div>
          </div>
          <div className="flex h-40 m-2 w-[80%]">
            <p className="m-3">{comment.content}</p>
          </div>
          {!loadingUser && (
            <button
              className="custom_button"
              onClick={() => setShowReplyForm(!showReplyForm)}
            >
              Reply
            </button>
          )}
        </div>
      </div>

      {showReplyForm && (
        <div className="flex flex-col w-[80%] ml-10 reply_box">
          <textarea
            className="invisible_box"
            placeholder="Write your reply..."
            value={replyContent}
            onChange={(e) => setReplyContent(e.target.value)}
          />
          <button
            className="p-2 mt-2 custom_button w-14"
            onClick={handleReplySubmit}
          >
            Reply
          </button>
        </div>
      )}

      {replies.length > 0 && (
        <div className="ml-10 w-full">
          {replies.map((reply) => (
            <Comment
              key={reply.comment_id}
              comment={reply}
              comments={comments}
              parentDebateId={parentDebateId}
              depth={depth + 1}
              loadingUser={loadingUser}
              addReply={addReply}
              currentUser={currentUser}
              currentProfilePic={currentProfilePic}
            />
          ))}
        </div>
      )}
    </div>
  );
}

