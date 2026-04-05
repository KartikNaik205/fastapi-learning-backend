import {useEffect, useState} from "react";

function App() {
  const[notes, setNotes] = useState([]);
  const[selectedNote, setSelectedNote] = useState(null);
  const[summary, setSummary] = useState("");
  const[cached, setCached] = useState(null);
  const [loading, setLoading] = useState(false);
  const [newTitle , setNewTitle] = useState("");
  const [newContent, setNewContent] = useState("");
  const [editMode, setEditMode] = useState(false);
  const [editTitle, setEditTitle] = useState("");
  const [editContent, setEditContent] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/notes")
    .then((res) => res.json())
    .then((data) => setNotes(data))
    .catch(() => console.log("Failed to fetch notes"));
  }, []);

  const handleSummarize = async (id) => {
    setLoading(true);

    try{
      const res = await fetch(`http://localhost:8000/notes/${id}/summarize`, {
       method: "POST",
    });
    
    const data = await res.json();

    setSummary(data.summary);
    setCached(data.cached);
  } catch(err) {
    console.error(err);
    alert("Failed to summarize");
  } finally {
     setLoading(false);
  }
 };

 const handleCreateNote = async () => {
  if(!newTitle || !newContent) {
    alert("Please fill both fields");
    return;
  }

  try {
    const res = await fetch("http://localhost:8000/notes", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: newTitle,
        content: newContent,
        user_id: 1,
      }),
    });

    const data = await res.json();

    setNotes([...notes, data]);

    setNewTitle("");
    setNewContent("");
  } catch (err) {
    console.error(err);
    alert("Failed to create note");
  }
 };

 const handleDelete = async(id) => {
  try{
    await fetch(`http://localhost:8000/notes/${id}`, {
      method: "DELETE",
    });

    setNotes(notes.filter((note) => note.id !== id));

    if (selectedNote?.id === id) {
      setSelectedNote(null);
      setSummary("");
      setCached(null);
    }

  } catch (err) {
    console.error(err);
    alert("Failed to delete note");
  }
 }

 const handleEdit = (note) => {
  setSelectedNote(note);
  setEditMode(true);
  setEditTitle(note.title);
  setEditContent(note.content);
 };

 const handleUpdateNote = async () => {
  try{
    const res = await fetch(`http://localhost:8000/notes/${selectedNote.id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: editTitle,
        content: editContent,
      }),
    });

    const updated = await res.json();

    setNotes(notes.map((n) => (n.id === updated.id ? updated : n)));

    setSelectedNote(updated);

    setEditMode(false);
  } catch (err) {
    console.error(err);
    alert("Failed to update note")
  }
};
 

  return (
    <div className="min-h-screen bg-black text-green-400 p-8">
      <h1 className="text-3xl font-bold mb-6">AI Notes</h1>

      <div className="mb-6 border border-green-700 p-4">
        <h2 className="text-xl mb-3">Create Note</h2>

        <input 
          type="text"
          placeholder="Title"
          className="w-full p-2 mb-2 bg-black border border-green-500"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
        />

        <textarea
          placeholder="Content"
          className="w-full p-2 mb-2 bg-black border border-green-500"
          value={newContent}
          onChange={(e) => setNewContent(e.target.value)}
        />

        <button
          onClick={handleCreateNote}
          className="bg-green-600 px-4 py-2 rounded hover:bg-green-500"
        >
          Add Note
        </button>     
      </div>

      <div className="grid grid-cols-2 gap-6">

        {/* LEFT SIDE - NOTES */}
        <div>
          <h2 className="text-xl mb-4">Notes</h2>
          {notes.map((note) => (
            <div 
            key={note.id}
            className="border border-green-500 p-3 mb-3 "
            >
              <div
              className="cursor-pointer hover:bg-green-900"
              onClick={() => {
                setSelectedNote(note);
                setSummary("");
                setCached(null);
            }}
          >
            {note.title}
          </div>  

          <button
           onClick={() => handleDelete(note.id)}
           className="text-red-400 text-sm mt-2"
           >
            Delete
           </button>

           <button
             onClick={() => handleEdit(note)}
             className="text-yellow-400 text-sm mt-2 ml-4"
           >
            Edit
          </button>  
        </div>
      ))}
      

        {/* RIGHT SIDE -DETAILS */}
        <div>
          {selectedNote && (
            <>
              <h2 className="text-xl mb-2">{editMode ? editTitle : selectedNote.title}</h2>
              {editMode? (
                <>
                <input 
                  className="w-full p-2 mb-2 bg-black border border-green-500"
                  value = {editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  />

                 <textarea 
                  className="w-full p-2 mb-2 bg-black border border-green-500"
                  value={editContent}
                  onChange={(e) => setEditContent(e.target.value)}
                  />

                  <button
                   onClick={handleUpdateNote}
                   className="bg-yellow-500 text-black px-4 py-2 rounded"
                  >
                    Save
                  </button> 

                  <button
                   onClick={() => {setEditMode(false);
                    setEditTitle(selectedNote.title);
                    setEditContent(selectedNote.content);
                   }}
                   className="ml-2 text-red-400">
                   Cancel
                   </button>
                  </>
              ) : (
                <p className="mb-4">{selectedNote.content}</p>
              )} 
                   
              

              <button
               onClick={() => handleSummarize(selectedNote.id)}
               className="bg-green-600 px-4 py-2 rounded hover:bg-green-500"
               disabled={loading}
               >
                {loading ? "Summarizing..." : "Summarize"}
               </button>

               {
                summary && (
                  <div className="mt-4 border border-green-500 p-4">
                    <h3 className="mb-2 font-semibold">Summary</h3>
                    <p>{summary}</p>
                    <p className="text-sm mt-2">
                      Cached: {cached ? "Yes" : "No"}
                    </p>
                  </div>
                )}
            </>
          )}
        </div>
       </div>
      </div>
    </div>
  );
}

export default App;