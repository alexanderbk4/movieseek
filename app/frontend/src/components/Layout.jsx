import { Outlet } from 'react-router-dom'
import Navbar from './Navbar'
import Footer from './Footer'
import TailwindTest from './TailwindTest'

const Layout = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      {/* Tailwind Test Element */}
      <div className="p-4 m-4 bg-blue-500 text-white text-center rounded-xl shadow-lg">
        This is a test element with Tailwind CSS classes
      </div>

      {/* Tailwind CDN Test */}
      <div className="bg-green-500 text-white p-4 m-4 rounded-lg shadow-md text-center">
        This should be styled by Tailwind CDN
      </div>

      {/* Inline Styles Test */}
      <div style={{ 
        padding: '16px', 
        margin: '16px', 
        backgroundColor: 'red', 
        color: 'white', 
        textAlign: 'center',
        borderRadius: '12px',
        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)'
      }}>
        This element uses inline styles
      </div>

      {/* Plain CSS Test */}
      <div className="plain-css-box">
        This element uses plain CSS classes
      </div>

      {/* Tailwind Test Component */}
      <TailwindTest />

      <Navbar />
      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="w-full max-w-7xl mx-auto">
          <Outlet />
        </div>
      </main>
      <Footer />
    </div>
  )
}

export default Layout 