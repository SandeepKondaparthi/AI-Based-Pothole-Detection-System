import Header from '../components/Header'
import Footer from '../components/Footer'

const ContactPage = () => {
  return (
    <div className="bg-background-light dark:bg-background-dark min-h-screen text-[#111418] dark:text-white">
      <Header showAuthButtons={true} />
      
      <main className="flex-1 flex justify-center py-16 px-4">
        <div className="layout-content-container flex flex-col max-w-[900px] w-full gap-12">
          {/* Page Heading */}
          <div className="flex flex-col gap-3">
            <h1 className="text-[#111418] dark:text-white text-4xl font-black leading-tight tracking-[-0.033em]">
              Contact Us
            </h1>
            <p className="text-[#617589] dark:text-gray-400 text-lg font-normal leading-normal">
              Have questions or feedback? Get in touch with our team.
            </p>
          </div>

          {/* Contact Info Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Email */}
            <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-[#dbe0e6] dark:border-gray-800 p-8 flex flex-col gap-4">
              <span className="material-symbols-outlined text-primary text-4xl">mail</span>
              <h3 className="text-lg font-bold">Email</h3>
              <p className="text-gray-600 dark:text-gray-400">
                For general inquiries and support
              </p>
              <a href="mailto:support@roadcare.local" className="text-primary font-semibold hover:underline">
                support@roadcare.local
              </a>
            </div>

            {/* Phone */}
            <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-[#dbe0e6] dark:border-gray-800 p-8 flex flex-col gap-4">
              <span className="material-symbols-outlined text-primary text-4xl">phone</span>
              <h3 className="text-lg font-bold">Phone</h3>
              <p className="text-gray-600 dark:text-gray-400">
                For urgent matters and complaints
              </p>
              <a href="tel:+1-800-ROADCARE" className="text-primary font-semibold hover:underline">
                +1-800-ROADCARE
              </a>
            </div>

            {/* Address */}
            <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-[#dbe0e6] dark:border-gray-800 p-8 flex flex-col gap-4">
              <span className="material-symbols-outlined text-primary text-4xl">location_on</span>
              <h3 className="text-lg font-bold">Address</h3>
              <p className="text-gray-600 dark:text-gray-400">
                Visit our office
              </p>
              <a href="https://maps.google.com" target="_blank" rel="noopener noreferrer" className="text-primary font-semibold hover:underline">
                View on Maps
              </a>
            </div>
          </div>

          {/* Contact Form */}
          <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-[#dbe0e6] dark:border-gray-800 p-8 flex flex-col gap-6">
            <h2 className="text-2xl font-bold">Send us a Message</h2>
            
            <form className="flex flex-col gap-4">
              {/* Name */}
              <div className="flex flex-col gap-2">
                <label htmlFor="name" className="font-semibold text-sm">
                  Your Name
                </label>
                <input
                  type="text"
                  id="name"
                  placeholder="John Doe"
                  data-testid="contact-name"
                  className="w-full px-4 py-3 rounded-lg border border-[#dbe0e6] dark:border-gray-700 bg-white dark:bg-gray-800 text-[#111418] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>

              {/* Email */}
              <div className="flex flex-col gap-2">
                <label htmlFor="email" className="font-semibold text-sm">
                  Email Address
                </label>
                <input
                  type="email"
                  id="email"
                  placeholder="john@example.com"
                  data-testid="contact-email"
                  className="w-full px-4 py-3 rounded-lg border border-[#dbe0e6] dark:border-gray-700 bg-white dark:bg-gray-800 text-[#111418] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>

              {/* Subject */}
              <div className="flex flex-col gap-2">
                <label htmlFor="subject" className="font-semibold text-sm">
                  Subject
                </label>
                <select
                  id="subject"
                  data-testid="contact-subject"
                  className="w-full px-4 py-3 rounded-lg border border-[#dbe0e6] dark:border-gray-700 bg-white dark:bg-gray-800 text-[#111418] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option>General Inquiry</option>
                  <option>Report a Bug</option>
                  <option>Feature Request</option>
                  <option>Partnership</option>
                  <option>Other</option>
                </select>
              </div>

              {/* Message */}
              <div className="flex flex-col gap-2">
                <label htmlFor="message" className="font-semibold text-sm">
                  Message
                </label>
                <textarea
                  id="message"
                  placeholder="Tell us what's on your mind..."
                  rows="6"
                  data-testid="contact-message"
                  className="w-full px-4 py-3 rounded-lg border border-[#dbe0e6] dark:border-gray-700 bg-white dark:bg-gray-800 text-[#111418] dark:text-white focus:outline-none focus:ring-2 focus:ring-primary resize-none"
                />
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                data-testid="contact-submit"
                className="w-full bg-primary text-white py-3 rounded-lg font-semibold hover:bg-primary/90 transition-colors"
              >
                Send Message
              </button>
            </form>
          </div>

          {/* FAQ Section */}
          <div className="flex flex-col gap-6">
            <h2 className="text-2xl font-bold">Frequently Asked Questions</h2>
            
            <div className="space-y-4">
              <div className="bg-white dark:bg-gray-900 rounded-lg border border-[#dbe0e6] dark:border-gray-800 p-6">
                <h4 className="font-semibold mb-2">How accurate is the AI detection?</h4>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  Our AI system achieves 90%+ accuracy for pothole detection using advanced computer vision techniques.
                </p>
              </div>

              <div className="bg-white dark:bg-gray-900 rounded-lg border border-[#dbe0e6] dark:border-gray-800 p-6">
                <h4 className="font-semibold mb-2">How long does repair take?</h4>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  Repair timelines vary by location and severity. You can track the status through the app.
                </p>
              </div>

              <div className="bg-white dark:bg-gray-900 rounded-lg border border-[#dbe0e6] dark:border-gray-800 p-6">
                <h4 className="font-semibold mb-2">Can I report anonymously?</h4>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  You need an account to report, but you can make your reports private in settings.
                </p>
              </div>

              <div className="bg-white dark:bg-gray-900 rounded-lg border border-[#dbe0e6] dark:border-gray-800 p-6">
                <h4 className="font-semibold mb-2">Is the app free?</h4>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  Yes! RoadCare is completely free for citizens and government agencies.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}

export default ContactPage
