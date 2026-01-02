import { useState } from 'react';

interface AddTodoProps {
  onAddTodo: (content: string) => void;
}

export default function AddTodo({ onAddTodo }: AddTodoProps) {
  const [content, setContent] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (content.trim()) {
      onAddTodo(content);
      setContent('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="flex">
        <input
          type="text"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Add a new todo..."
          className="flex-1 px-4 py-3 bg-white/10 border border-white/30 rounded-l-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent backdrop-blur-sm"
        />
        <button
          type="submit"
          className="px-6 py-3 text-sm font-medium text-white bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 rounded-r-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-300 shadow-md"
        >
          Add
        </button>
      </div>
    </form>
  );
}