export default function CurrentItem({ task }) {
  if (!task) return <p>No pending tasks. All done!</p>;

  return (
    <section className="current-item">
      <h2>Current Item</h2>
      <div className="item-header">
        {/* This logic works for URLs, local files, and empty images */}
        <img 
          src={
            task.item.image && task.item.image.startsWith('http') 
              ? task.item.image 
              : (task.item.image ? `http://127.0.0.1:8000${task.item.image}` : 'https://via.placeholder.com/150')
          } 
          alt={task.item.name} 
        />
        <div>
          <p className="sku">SKU: {task.item.sku}</p>
          <h3>{task.item.name}</h3>
          <p>{task.item.description}</p>
          <button className="btn-details">View Details</button>
        </div>
      </div>
    </section>
  );
}