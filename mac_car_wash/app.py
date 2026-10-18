from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import os
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Flask configuration
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'your-email@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'your-app-password')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME', 'your-email@gmail.com')

# Initialize Flask-Mail
mail = Mail(app)

# Business configuration
BUSINESS_EMAIL = os.getenv('BUSINESS_EMAIL', 'info@macmobilecarwash.com')
BUSINESS_PHONE = '+971 5011 34356'
BUSINESS_NAME = 'MAC Mobile Car Washing'

# Company Information
COMPANY_INFO = {
    'name': BUSINESS_NAME,
    'phone': BUSINESS_PHONE,
    'email': BUSINESS_EMAIL,
    'experience': '10+ years',
    'customers': '10,000+',
    'location': 'Dubai, UAE',
    'website': 'https://macmobilecarwash.com'
}

# Pricing/Services Information (structured for template compatibility)
PRICING = {
    'single_wash': {
        'silver': {
            'name': 'Silver Wash',
            'price': 55,
            'type': 'One Time Service',
            'description': 'Basic exterior wash with premium products'
        },
        'gold': {
            'name': 'Gold Wash',
            'price': 75,
            'type': 'One Time Service',
            'description': 'Complete exterior and interior cleaning'
        }
    },
    'monthly': {
        'green': {
            'name': 'Green Package',
            'price': 180,
            'type': 'Monthly Package',
            'description': 'Regular monthly car wash service'
        },
        'blue': {
            'name': 'Blue Package',
            'price': 240,
            'type': 'Monthly Package',
            'description': 'Premium monthly car wash with detailing'
        }
    },
    'yearly': {
        'green': {
            'name': 'Green Package',
            'price': 1500,
            'original': 2160,
            'type': '1 Year Package',
            'description': 'Annual subscription with 30% discount'
        },
        'blue': {
            'name': 'Blue Package',
            'price': 2000,
            'original': 2880,
            'type': '1 Year Package',
            'description': 'Premium annual subscription with 30% discount'
        }
    }
}

# Services for API and form handling
SERVICES = {
    'silver': {
        'name': 'Silver Wash',
        'price': 55,
        'type': 'One Time Service',
        'description': 'Basic exterior wash with premium products'
    },
    'gold': {
        'name': 'Gold Wash',
        'price': 75,
        'type': 'One Time Service',
        'description': 'Complete exterior and interior cleaning'
    },
    'green-monthly': {
        'name': 'Green Package',
        'price': 180,
        'type': 'Monthly Package',
        'description': 'Regular monthly car wash service'
    },
    'blue-monthly': {
        'name': 'Blue Package',
        'price': 240,
        'type': 'Monthly Package',
        'description': 'Premium monthly car wash with detailing'
    },
    'green-yearly': {
        'name': 'Green Package',
        'price': 1500,
        'original_price': 2160,
        'type': 'Yearly Package (30% Off)',
        'description': 'Annual subscription with 30% discount'
    },
    'blue-yearly': {
        'name': 'Blue Package',
        'price': 2000,
        'original_price': 2880,
        'type': 'Yearly Package (30% Off)',
        'description': 'Premium annual subscription with 30% discount'
    }
}

# Service Features
SERVICE_FEATURES = [
    {
        'title': 'Innovative Washing',
        'description': 'Advanced spray and wipe technology for spotless results',
        'icon': '🚿'
    },
    {
        'title': 'Safety Materials',
        'description': 'Premium eco-friendly products safe for your car',
        'icon': '🛡️'
    },
    {
        'title': 'Modern Equipment',
        'description': 'State-of-the-art mobile car washing equipment',
        'icon': '⚙️'
    },
    {
        'title': 'Extensive Cleaning',
        'description': 'Comprehensive interior and exterior detailing',
        'icon': '✨'
    }
]

# Customer Testimonials
TESTIMONIALS = [
    {
        'name': 'Reshmi',
        'text': 'Very meticulous and great attention to detail!!! Second time experience with them after a long time and they have maintained their high standard mobile car wash.',
        'rating': 5
    },
    {
        'name': 'Joji',
        'text': 'Excellent mobile car wash service received by MAC. Their hard work and cleaning service was awesome and I would recommend to all my friends. All the best!',
        'rating': 5
    },
    {
        'name': 'Ahmed Al-Mansouri',
        'text': 'Professional service at my office building. Always on time and excellent quality. Highly recommended for corporate clients.',
        'rating': 5
    },
    {
        'name': 'Sarah Johnson',
        'text': 'Amazing service! They come to my villa and do such a thorough job. My car looks brand new every time. Worth every dirham!',
        'rating': 5
    }
]

# ==================== ROUTES ====================

@app.route('/')
def home():
    """Home page with all necessary data"""
    return render_template('index.html', 
                         company=COMPANY_INFO, 
                         pricing=PRICING,  # For template compatibility
                         services=SERVICE_FEATURES,  # Service features
                         testimonials=TESTIMONIALS)

@app.route('/services')
def services_page():
    """Services page"""
    return render_template('services.html', 
                         company=COMPANY_INFO,
                         pricing=PRICING,
                         services=SERVICE_FEATURES,
                         features=SERVICE_FEATURES)

@app.route('/pricing')
def pricing_page():
    """Pricing page"""
    return render_template('pricing.html', 
                         company=COMPANY_INFO,
                         pricing=PRICING,
                         services=SERVICES)

@app.route('/contact')
def contact_page():
    """Contact page"""
    return render_template('contact.html', 
                         company=COMPANY_INFO,
                         pricing=PRICING,
                         services=SERVICES)

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    """Handle contact form submission and send emails"""
    try:
        data = request.get_json()
        
        # Extract and validate form data
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        customer_email = data.get('email', '').strip()
        service_type = data.get('service', '').strip()
        customer_message = data.get('message', '').strip()
        
        # Validate required fields
        if not name:
            return jsonify({
                'success': False,
                'message': 'Please provide your name'
            }), 400
            
        if not phone:
            return jsonify({
                'success': False,
                'message': 'Please provide your phone number'
            }), 400
            
        if not customer_email:
            return jsonify({
                'success': False,
                'message': 'Please provide your email address'
            }), 400
        
        # Validate email format
        if '@' not in customer_email or '.' not in customer_email:
            return jsonify({
                'success': False,
                'message': 'Please provide a valid email address'
            }), 400
        
        # Get service details
        service_info = SERVICES.get(service_type, {
            'name': 'General Inquiry',
            'price': 'Contact for pricing',
            'type': 'Service Inquiry',
            'description': 'General service inquiry'
        })
        
        # Save booking data to file
        booking_saved = save_booking_data(name, phone, customer_email, service_type, customer_message, service_info)
        
        # Send emails
        booking_email_sent = send_booking_email(name, phone, customer_email, service_info, customer_message)
        confirmation_email_sent = send_customer_confirmation(customer_email, name, service_info)
        
        # Determine success message based on email status
        if booking_email_sent and confirmation_email_sent:
            message = 'Thank you for your booking! We will contact you within 2 hours to confirm your appointment. Please check your email for confirmation details.'
        elif booking_email_sent or confirmation_email_sent:
            message = 'Thank you for your booking! We have received your request and will contact you within 2 hours.'
        else:
            message = 'Thank you for contacting us! We have received your request and will get back to you soon. If urgent, please call us directly.'
        
        return jsonify({
            'success': True,
            'message': message,
            'booking_id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'service': service_info['name']
        })
        
    except Exception as e:
        print(f"❌ Error handling contact form: {e}")
        return jsonify({
            'success': False,
            'message': f'Something went wrong. Please try calling us directly at {BUSINESS_PHONE} for immediate assistance.'
        }), 500

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    """Enhanced chatbot with comprehensive responses"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower().strip()
        
        if not user_message:
            return jsonify({'response': 'Please type a message! I\'m here to help with your car wash needs.'})
        
        # Enhanced chatbot responses with better matching
        responses = {
            # Greetings
            'hello': f"Hello! Welcome to {BUSINESS_NAME}. How can I help you today? Ask me about pricing, services, booking, or location!",
            'hi': f"Hi there! I'm your virtual assistant for {BUSINESS_NAME}. What would you like to know about our car washing services?",
            'hey': f"Hey! Great to see you here. I can help you with pricing, booking, or any questions about our mobile car wash services.",
            
            # Pricing queries
            'pricing': f"💰 Our Current Pricing:\n• Silver Wash: AED {SERVICES['silver']['price']} (One Time)\n• Gold Wash: AED {SERVICES['gold']['price']} (One Time)\n• Green Monthly: AED {SERVICES['green-monthly']['price']}\n• Blue Monthly: AED {SERVICES['blue-monthly']['price']}\n• Yearly packages available with 30% discount! Call {BUSINESS_PHONE} for details.",
            'price': f"Our services start from AED {SERVICES['silver']['price']} for Silver Wash. Monthly packages from AED {SERVICES['green-monthly']['price']}. Special yearly packages with 30% discount available!",
            'cost': f"Affordable pricing: Silver (AED {SERVICES['silver']['price']}), Gold (AED {SERVICES['gold']['price']}), Monthly packages from AED {SERVICES['green-monthly']['price']}. Great value for professional service!",
            'cheap': f"We offer competitive rates starting from AED {SERVICES['silver']['price']} for Silver Wash. Monthly packages provide better value from AED {SERVICES['green-monthly']['price']}.",
            
            # Services
            'service': f"🚗 Our Services Include:\n• Mobile Car Washing (We come to you!)\n• Exterior & Interior Cleaning\n• Premium Detailing\n• Corporate Services\n• Villa & Tower Services\nAll with eco-friendly products and modern equipment!",
            'services': f"We offer comprehensive mobile car wash services: Silver Wash (basic), Gold Wash (premium), Monthly packages for regular customers, and discounted yearly packages. All services performed at your location!",
            'wash': f"We provide professional mobile car washing services across Dubai/UAE. From basic exterior wash to complete detailing - we bring everything to your location!",
            'clean': f"Professional cleaning services include exterior washing, interior vacuuming, dashboard cleaning, window cleaning, and tire shine. We use only premium, eco-friendly products.",
            'detail': f"Our detailing service includes thorough interior and exterior cleaning, premium wax application, tire shine, and dashboard conditioning. Available in Gold package and monthly subscriptions.",
            
            # Location & Coverage
            'location': f"📍 Service Areas: We cover all of Dubai and UAE including:\n• Villas & Residential Areas\n• Corporate Buildings\n• Hotels & Resorts\n• Residential Towers\n• Shopping Malls\nWe come to your location with all equipment!",
            'dubai': f"Yes! We serve all areas of Dubai including Downtown, Marina, JBR, Jumeirah, Deira, Bur Dubai, and surrounding areas. Mobile service means we come to you!",
            'area': f"We provide mobile car wash services across Dubai, Sharjah, Ajman, and other UAE emirates. Residential areas, offices, hotels - wherever you need us!",
            'where': f"We operate throughout Dubai and UAE. Just call {BUSINESS_PHONE} and we'll confirm if we serve your specific area. Most likely, we do!",
            
            # Booking
            'booking': f"📞 Easy Booking Options:\n• Call us: {BUSINESS_PHONE}\n• Use our contact form on the website\n• WhatsApp us for quick booking\nWe'll arrange a convenient time and come to your location!",
            'book': f"To book our service, simply call {BUSINESS_PHONE} or fill out our contact form. We'll schedule a convenient time and bring all equipment to your location!",
            'appointment': f"Schedule your appointment by calling {BUSINESS_PHONE}. We offer flexible timing 7 days a week to fit your schedule. Same-day service often available!",
            'schedule': f"We work around your schedule! Call {BUSINESS_PHONE} to arrange a convenient time. We operate 7 days a week across Dubai/UAE.",
            
            # Contact Information
            'contact': f"📞 Contact Information:\n• Phone: {BUSINESS_PHONE} (Call/WhatsApp)\n• Email: {BUSINESS_EMAIL}\n• We're available 7 days a week\n• Service across Dubai/UAE",
            'phone': f"Our phone number is {BUSINESS_PHONE}. You can call or WhatsApp us anytime for bookings, quotes, or questions!",
            'number': f"Call us at {BUSINESS_PHONE} for immediate assistance. We're available 7 days a week for bookings and inquiries!",
            'whatsapp': f"Yes! You can WhatsApp us at {BUSINESS_PHONE} for quick booking and inquiries. We respond fast!",
            
            # Experience & Credentials
            'experience': f"🏆 Our Track Record:\n• {COMPANY_INFO['experience']} in mobile car washing\n• Over {COMPANY_INFO['customers']} satisfied customers\n• Professional, insured staff\n• Modern equipment & eco-friendly products\n• Serving Dubai/UAE",
            'professional': f"Absolutely! We're a licensed, professional mobile car wash company with {COMPANY_INFO['experience']} experience and {COMPANY_INFO['customers']} happy customers in Dubai/UAE.",
            'trust': f"You can trust us! We have {COMPANY_INFO['experience']} experience, {COMPANY_INFO['customers']} satisfied customers, fully insured staff, and professional-grade equipment.",
            
            # Timing & Availability
            'time': f"⏰ We operate 7 days a week across Dubai/UAE. Flexible timing from morning to evening. Call {BUSINESS_PHONE} to schedule your preferred time slot!",
            'available': f"We're available 7 days a week! Flexible scheduling to fit your busy lifestyle. Same-day service often available - call {BUSINESS_PHONE}!",
            'hours': f"We work 7 days a week with flexible hours to accommodate your schedule. Call {BUSINESS_PHONE} to arrange your preferred time!",
            
            # Payment & Pricing Details
            'payment': f"💳 Payment Options:\n• Cash (paid after service completion)\n• Card payments accepted\n• Payment only after you're satisfied with our service\n• No hidden charges!",
            'monthly': f"📅 Monthly Packages:\n• Green Package: AED {SERVICES['green-monthly']['price']}/month\n• Blue Package: AED {SERVICES['blue-monthly']['price']}/month\n• Regular service, consistent quality, better value!",
            'yearly': f"🎉 Yearly Packages (30% OFF!):\n• Green Yearly: AED {SERVICES['green-yearly']['price']} (Save AED {SERVICES['green-yearly']['original_price'] - SERVICES['green-yearly']['price']}!)\n• Blue Yearly: AED {SERVICES['blue-yearly']['price']} (Save AED {SERVICES['blue-yearly']['original_price'] - SERVICES['blue-yearly']['price']}!)",
            'discount': f"💰 Special Offer: 30% discount on yearly packages! Green: AED {SERVICES['green-yearly']['price']} (was {SERVICES['green-yearly']['original_price']}), Blue: AED {SERVICES['blue-yearly']['price']} (was {SERVICES['blue-yearly']['original_price']}).",
            
            # Equipment & Products
            'equipment': f"🔧 We bring everything:\n• Professional washing equipment\n• Our own water supply\n• Eco-friendly cleaning products\n• Vacuum cleaners\n• Microfiber cloths\nYou don't need to provide anything!",
            'products': f"We use premium, eco-friendly cleaning products that are safe for your car and the environment. Professional-grade equipment ensures excellent results every time!",
            'water': f"We bring our own water supply! No need to use your water. Our mobile units are fully equipped for complete independence.",
            
            # Special Services
            'corporate': f"🏢 Corporate Services Available!\n• Office building services\n• Hotel partnerships\n• Bulk discounts for multiple cars\n• Regular scheduled services\nCall {BUSINESS_PHONE} for corporate rates!",
            'villa': f"🏠 Villa Services:\n• We serve all villa communities in Dubai\n• Convenient driveway service\n• Flexible timing\n• Regular monthly packages available\nPerfect for villa residents!",
            
            # Gratitude responses
            'thank': f"You're very welcome! Feel free to ask any other questions or call us at {BUSINESS_PHONE}. We're here to make your car look amazing!",
            'thanks': f"My pleasure! If you need anything else or want to book our service, just call {BUSINESS_PHONE}. We'd love to serve you!",
            
            # Farewell
            'bye': f"Goodbye! Thank you for considering {BUSINESS_NAME}. Remember, we're just a call away at {BUSINESS_PHONE} for the best mobile car wash in Dubai! 🚗✨",
            'goodbye': f"Take care! Don't forget - {BUSINESS_NAME} is here whenever you need professional car wash service. Call {BUSINESS_PHONE}!",
            
            # Default response
            'default': f"Thank you for your message! For specific inquiries about our mobile car wash services, pricing, or booking, please call us at {BUSINESS_PHONE}. We're here to help make your car shine! 🚗✨"
        }
        
        # Advanced keyword matching
        response = responses['default']
        
        # Multi-keyword matching for better responses
        if any(word in user_message for word in ['price', 'cost', 'rate', 'charge', 'fee', 'expensive', 'cheap']):
            response = responses['pricing']
        elif any(word in user_message for word in ['book', 'appointment', 'schedule', 'reserve', 'when']):
            response = responses['booking']
        elif any(word in user_message for word in ['contact', 'phone', 'call', 'number', 'reach']):
            response = responses['contact']
        elif any(word in user_message for word in ['service', 'wash', 'clean', 'detail']):
            response = responses['services']
        elif any(word in user_message for word in ['location', 'area', 'where', 'dubai', 'uae']):
            response = responses['location']
        elif any(word in user_message for word in ['monthly', 'month', 'regular']):
            response = responses['monthly']
        elif any(word in user_message for word in ['yearly', 'year', 'annual', 'discount']):
            response = responses['yearly']
        elif any(word in user_message for word in ['corporate', 'office', 'business', 'company']):
            response = responses['corporate']
        elif any(word in user_message for word in ['villa', 'home', 'house', 'residential']):
            response = responses['villa']
        elif any(word in user_message for word in ['equipment', 'tools', 'water', 'products']):
            response = responses['equipment']
        elif any(word in user_message for word in ['time', 'hours', 'available', 'open']):
            response = responses['time']
        elif any(word in user_message for word in ['payment', 'pay', 'cash', 'card']):
            response = responses['payment']
        elif any(word in user_message for word in ['experience', 'professional', 'trust', 'reliable']):
            response = responses['experience']
        elif any(word in user_message for word in ['hello', 'hi', 'hey']):
            # Check for specific greeting
            for greeting in ['hello', 'hi', 'hey']:
                if greeting in user_message:
                    response = responses[greeting]
                    break
        elif any(word in user_message for word in ['thank', 'thanks']):
            response = responses['thank']
        elif any(word in user_message for word in ['bye', 'goodbye']):
            response = responses['bye']
        else:
            # Single keyword matching as fallback
            for keyword, reply in responses.items():
                if keyword in user_message:
                    response = reply
                    break
        
        return jsonify({'response': response})
        
    except Exception as e:
        print(f"❌ Chatbot error: {e}")
        return jsonify({
            'response': f"I apologize, but I encountered an error. Please contact us directly at {BUSINESS_PHONE} for immediate assistance with your car wash needs!"
        })

@app.route('/api/quote', methods=['POST'])
def get_quote():
    """Get detailed quote for specific service"""
    try:
        data = request.get_json()
        service_type = data.get('service', '').strip()
        
        if service_type in SERVICES:
            service = SERVICES[service_type]
            quote_response = {
                'success': True,
                'service': service['name'],
                'price': f"AED {service['price']}",
                'type': service['type'],
                'description': service.get('description', ''),
                'includes': get_service_includes(service_type)
            }
            
            # Add savings info for yearly packages
            if 'yearly' in service_type and 'original_price' in service:
                quote_response['savings'] = f"AED {service['original_price'] - service['price']}"
                quote_response['original_price'] = f"AED {service['original_price']}"
            
            return jsonify(quote_response)
        else:
            return jsonify({
                'success': False,
                'message': 'Service not found. Please contact us for custom pricing.',
                'phone': BUSINESS_PHONE
            })
            
    except Exception as e:
        print(f"❌ Quote error: {e}")
        return jsonify({
            'success': False,
            'message': 'Error getting quote. Please contact us directly.',
            'phone': BUSINESS_PHONE
        })

def get_service_includes(service_type):
    """Get what's included in each service type"""
    includes = {
        'silver': [
            'Exterior wash and rinse',
            'Premium soap and products',
            'Tire cleaning',
            'Basic interior vacuum',
            'Window cleaning (exterior)'
        ],
        'gold': [
            'Everything in Silver plus:',
            'Complete interior cleaning',
            'Dashboard conditioning',
            'Interior window cleaning',
            'Air freshener',
            'Tire shine application'
        ],
        'green-monthly': [
            'Silver wash service',
            'Monthly consistency',
            'Priority booking',
            'Same professional team'
        ],
        'blue-monthly': [
            'Gold wash service',
            'Monthly consistency', 
            'Priority booking',
            'Same professional team',
            'Special monthly discounts'
        ],
        'green-yearly': [
            'Silver wash service',
            '12 services per year',
            '30% discount savings',
            'Priority booking',
            'Consistent quality'
        ],
        'blue-yearly': [
            'Gold wash service',
            '12 services per year', 
            '30% discount savings',
            'Priority booking',
            'Premium treatment all year'
        ]
    }
    return includes.get(service_type, ['Professional car wash service'])

def save_booking_data(name, phone, email, service_type, message, service_info):
    """Save booking data to JSON file for record keeping"""
    try:
        booking_data = {
            'booking_id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'timestamp': datetime.now().isoformat(),
            'customer': {
                'name': name,
                'phone': phone,
                'email': email
            },
            'service': {
                'type': service_type,
                'name': service_info.get('name', 'Unknown'),
                'price': service_info.get('price', 'Unknown'),
                'package_type': service_info.get('type', 'Unknown'),
                'description': service_info.get('description', '')
            },
            'message': message,
            'status': 'pending',
            'source': 'website_contact_form'
        }
        
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Read existing bookings
        bookings_file = 'data/bookings.json'
        try:
            with open(bookings_file, 'r', encoding='utf-8') as f:
                bookings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            bookings = []
        
        # Add new booking
        bookings.append(booking_data)
        
        # Keep only last 1000 bookings to prevent file from getting too large
        if len(bookings) > 1000:
            bookings = bookings[-1000:]
        
        # Save updated bookings
        with open(bookings_file, 'w', encoding='utf-8') as f:
            json.dump(bookings, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Booking saved: {booking_data['booking_id']} - {name} - {service_info.get('name', 'Unknown service')}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving booking data: {e}")
        return False

def send_booking_email(name, phone, customer_email, service_info, customer_message):
    """Send detailed booking notification email to business owner"""
    try:
        msg = Message(
            subject=f'🚗 New Car Wash Booking from {name} - {service_info.get("name", "Unknown")}',
            recipients=[BUSINESS_EMAIL]
        )
        
        # Format service price
        price_display = f"AED {service_info['price']}" if isinstance(service_info['price'], (int, float)) else str(service_info['price'])
        
        msg.html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>New Booking - MAC Mobile Car Wash</title>
        </head>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background: #f5f5f5;">
            <div style="max-width: 650px; margin: 20px auto; background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.15);">
                
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 32px; font-weight: 700;">🚗 {BUSINESS_NAME}</h1>
                    <h2 style="color: white; margin: 15px 0 0 0; font-size: 22px; font-weight: 400;">New Booking Request</h2>
                    <div style="background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 25px; display: inline-block; margin-top: 15px;">
                        <span style="color: white; font-weight: 600;">Booking ID: {datetime.now().strftime('%Y%m%d%H%M%S')}</span>
                    </div>
                </div>
                
                <!-- Main Content -->
                <div style="padding: 40px 30px;">
                    
                    <!-- Customer Details -->
                    <div style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); padding: 25px; border-radius: 12px; margin-bottom: 30px; border-left: 5px solid #3b82f6;">
                        <h3 style="color: #1e40af; margin: 0 0 20px 0; font-size: 20px; display: flex; align-items: center;">
                            👤 Customer Information
                        </h3>
                        
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #374151; width: 35%;">Full Name:</td>
                                <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0; color: #1f2937; font-weight: 600;">{name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #374151;">Phone Number:</td>
                                <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                    <a href="tel:{phone}" style="color: #059669; text-decoration: none; font-weight: 700; font-size: 16px; background: #ecfdf5; padding: 5px 12px; border-radius: 20px; display: inline-block;">
                                        📞 {phone}
                                    </a>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #374151;">Email Address:</td>
                                <td style="padding: 12px 0; border-bottom: 1px solid #e2e8f0;">
                                    <a href="mailto:{customer_email}" style="color: #2563eb; text-decoration: none; font-weight: 500;">{customer_email}</a>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 12px 0; font-weight: 600; color: #374151;">Request Time:</td>
                                <td style="padding: 12px 0; color: #1f2937; font-weight: 500;">{datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <!-- Service Details -->
                    <div style="background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%); padding: 25px; border-radius: 12px; margin-bottom: 30px; border-left: 5px solid #10b981;">
                        <h3 style="color: #065f46; margin: 0 0 20px 0; font-size: 20px; display: flex; align-items: center;">
                            🛍️ Service Details
                        </h3>
                        
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 12px 0; border-bottom: 1px solid #d1fae5; font-weight: 600; color: #374151; width: 35%;">Service Name:</td>
                                <td style="padding: 12px 0; border-bottom: 1px solid #d1fae5; color: #065f46; font-weight: 700; font-size: 18px;">{service_info['name']}</td>
                            </tr>
                            <tr>
                                <td style="padding: 12px 0; border-bottom: 1px solid #d1fae5; font-weight: 600; color: #374151;">Package Type:</td>
                                <td style="padding: 12px 0; border-bottom: 1px solid #d1fae5; color: #374151;">{service_info['type']}</td>
                            </tr>
                            <tr>
                                <td style="padding: 12px 0; border-bottom: 1px solid #d1fae5; font-weight: 600; color: #374151;">Price:</td>
                                <td style="padding: 12px 0; border-bottom: 1px solid #d1fae5;">
                                    <span style="color: #dc2626; font-weight: 700; font-size: 20px; background: #fef2f2; padding: 5px 12px; border-radius: 20px; display: inline-block;">
                                        💰 {price_display}
                                    </span>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 12px 0; font-weight: 600; color: #374151;">Description:</td>
                                <td style="padding: 12px 0; color: #374151; font-style: italic;">{service_info.get('description', 'Professional car wash service')}</td>
                            </tr>
                        </table>
                    </div>
                    
                    {f'''
                    <!-- Customer Message -->
                    <div style="background: linear-gradient(135deg, #fef3c7 0%, #fef7cd 100%); border-left: 5px solid #f59e0b; padding: 25px; margin-bottom: 30px; border-radius: 12px;">
                        <h4 style="color: #92400e; margin: 0 0 15px 0; font-size: 18px; display: flex; align-items: center;">
                            💬 Customer Message
                        </h4>
                        <div style="background: white; padding: 20px; border-radius: 8px; border-left: 3px solid #f59e0b;">
                            <p style="color: #78350f; margin: 0; line-height: 1.8; font-size: 16px; font-style: italic;">
                                "{customer_message}"
                            </p>
                        </div>
                    </div>
                    ''' if customer_message.strip() else ''}
                    
                    <!-- Action Required -->
                    <div style="background: linear-gradient(135deg, #fef2f2 0%, #fef7f7 100%); padding: 25px; border-radius: 12px; border-left: 5px solid #ef4444; margin-bottom: 30px;">
                        <h4 style="color: #dc2626; margin: 0 0 15px 0; font-size: 18px;">
                            ⚡ ACTION REQUIRED
                        </h4>
                        <p style="color: #991b1b; margin: 0 0 15px 0; font-weight: 600; font-size: 16px;">
                            Please contact the customer within 2 hours to confirm the appointment and arrange timing.
                        </p>
                        <div style="background: white; padding: 15px; border-radius: 8px;">
                            <p style="color: #7f1d1d; margin: 0; font-weight: 500;">
                                ✓ Confirm service details<br>
                                ✓ Schedule convenient time<br>
                                ✓ Confirm location/address<br>
                                ✓ Send booking confirmation
                            </p>
                        </div>
                    </div>
                    
                    <!-- Quick Actions -->
                    <div style="background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%); padding: 25px; border-radius: 12px; text-align: center; border-left: 5px solid #3b82f6;">
                        <h3 style="color: #1e40af; margin: 0 0 20px 0; font-size: 18px;">⚡ Quick Contact Actions</h3>
                        <div style="margin-bottom: 20px;">
                            <a href="tel:{phone}" style="display: inline-block; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 30px; margin: 0 10px 15px 0; font-weight: 700; font-size: 16px; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4); transition: all 0.3s;">
                                📞 Call {name.split()[0]}
                            </a>
                            <a href="mailto:{customer_email}" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 30px; margin: 0 10px 15px 0; font-weight: 700; font-size: 16px; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4); transition: all 0.3s;">
                                ✉️ Email Customer
                            </a>
                        </div>
                        <div style="background: white; padding: 15px; border-radius: 8px; border-left: 3px solid #3b82f6;">
                            <p style="color: #1e40af; margin: 0; font-weight: 600; font-size: 15px;">
                                💡 Tip: Call first for immediate response, then follow up with email confirmation
                            </p>
                        </div>
                    </div>
                </div>
                
                <!-- Footer -->
                <div style="background: #1f2937; color: white; padding: 30px; text-align: center;">
                    <h3 style="margin: 0 0 15px 0; color: #4ade80; font-size: 20px;">{BUSINESS_NAME}</h3>
                    <p style="margin: 0 0 10px 0; color: #d1d5db; font-size: 16px; font-weight: 500;">Professional Mobile Car Washing & Detailing Service</p>
                    <div style="margin: 20px 0;">
                        <p style="margin: 0; color: #9ca3af; font-size: 14px;">
                            📞 {BUSINESS_PHONE} | ✉️ {BUSINESS_EMAIL}
                        </p>
                        <p style="margin: 5px 0 0 0; color: #9ca3af; font-size: 14px;">
                            🌐 macmobilecarwash.com | 📍 Dubai, UAE
                        </p>
                    </div>
                    <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #374151;">
                        <p style="margin: 0; color: #6b7280; font-size: 12px;">
                            This is an automated booking notification. Please respond to the customer promptly.
                        </p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        mail.send(msg)
        print(f"✅ Booking notification email sent successfully for {name} - {service_info.get('name', 'Unknown')}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send booking notification email: {e}")
        return False

def send_customer_confirmation(customer_email, customer_name, service_info):
    """Send professional booking confirmation email to customer"""
    try:
        msg = Message(
            subject=f'🎉 Booking Confirmed - {BUSINESS_NAME} | {service_info.get("name", "Car Wash Service")}',
            recipients=[customer_email]
        )
        
        # Format service price
        price_display = f"AED {service_info['price']}" if isinstance(service_info['price'], (int, float)) else str(service_info['price'])
        
        msg.html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Booking Confirmation - MAC Mobile Car Wash</title>
        </head>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background: #f5f5f5;">
            <div style="max-width: 650px; margin: 20px auto; background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.15);">
                
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 32px; font-weight: 700;">🚗 {BUSINESS_NAME}</h1>
                    <h2 style="color: white; margin: 15px 0 5px 0; font-size: 24px; font-weight: 400;">Booking Confirmed! 🎉</h2>
                    <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 16px;">We're excited to serve you!</p>
                </div>
                
                <!-- Main Content -->
                <div style="padding: 40px 30px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h3 style="color: #2563eb; margin: 0 0 10px 0; font-size: 24px;">Hi {customer_name}! 👋</h3>
                        <p style="font-size: 18px; line-height: 1.6; color: #374151; margin-bottom: 0;">
                            Thank you for choosing <strong style="color: #2563eb;">{BUSINESS_NAME}</strong>! 
                        </p>
                        <p style="font-size: 16px; color: #6b7280; margin: 10px 0 0 0;">
                            We've received your booking request and we're excited to make your car shine!
                        </p>
                    </div>
                    
                    <!-- Service Details -->
                    <div style="background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%); padding: 30px; border-radius: 15px; border-left: 5px solid #10b981; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.1);">
                        <h4 style="color: #065f46; margin: 0 0 20px 0; font-size: 20px; text-align: center;">
                            🛍️ Your Service Details
                        </h4>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 15px 0; border-bottom: 2px solid #d1fae5; font-weight: 600; color: #374151; width: 40%; font-size: 16px;">Service Selected:</td>
                                <td style="padding: 15px 0; border-bottom: 2px solid #d1fae5; color: #065f46; font-weight: 700; font-size: 18px;">{service_info['name']}</td>
                            </tr>
                            <tr>
                                <td style="padding: 15px 0; border-bottom: 2px solid #d1fae5; font-weight: 600; color: #374151; font-size: 16px;">Package Type:</td>
                                <td style="padding: 15px 0; border-bottom: 2px solid #d1fae5; color: #374151; font-size: 16px;">{service_info['type']}</td>
                            </tr>
                            <tr>
                                <td style="padding: 15px 0; border-bottom: 2px solid #d1fae5; font-weight: 600; color: #374151; font-size: 16px;">Service Price:</td>
                                <td style="padding: 15px 0; border-bottom: 2px solid #d1fae5;">
                                    <span style="color: #dc2626; font-weight: 700; font-size: 22px; background: #fef2f2; padding: 8px 16px; border-radius: 25px; display: inline-block;">
                                        💰 {price_display}
                                    </span>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 15px 0; font-weight: 600; color: #374151; font-size: 16px;">Request Date:</td>
                                <td style="padding: 15px 0; color: #374151; font-weight: 500; font-size: 16px;">{datetime.now().strftime('%A, %B %d, %Y')}</td>
                            </tr>
                        </table>
                        
                        <div style="background: white; padding: 20px; border-radius: 10px; margin-top: 20px; border-left: 3px solid #10b981;">
                            <p style="color: #065f46; margin: 0; font-weight: 600; font-size: 16px; text-align: center;">
                                ✨ {service_info.get('description', 'Professional mobile car wash service at your location')} ✨
                            </p>
                        </div>
                    </div>
                    
                    <!-- What's Next -->
                    <div style="background: linear-gradient(135deg, #fef3c7 0%, #fef7cd 100%); padding: 30px; border-radius: 15px; border-left: 5px solid #f59e0b; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(245, 158, 11, 0.1);">
                        <h4 style="color: #92400e; margin: 0 0 20px 0; font-size: 20px; text-align: center;">
                            ⏰ What happens next?
                        </h4>
                        <div style="background: white; padding: 20px; border-radius: 10px;">
                            <ul style="color: #78350f; line-height: 2; margin: 0; padding-left: 0; list-style: none; font-size: 16px;">
                                <li style="margin-bottom: 12px; padding-left: 30px; position: relative;">
                                    <span style="position: absolute; left: 0; color: #f59e0b; font-weight: bold;">1️⃣</span>
                                    <strong>Within 2 hours:</strong> Our team will contact you to confirm your appointment
                                </li>
                                <li style="margin-bottom: 12px; padding-left: 30px; position: relative;">
                                    <span style="position: absolute; left: 0; color: #f59e0b; font-weight: bold;">2️⃣</span>
                                    <strong>Scheduling:</strong> We'll arrange a convenient time that works perfectly for you
                                </li>
                                <li style="margin-bottom: 12px; padding-left: 30px; position: relative;">
                                    <span style="position: absolute; left: 0; color: #f59e0b; font-weight: bold;">3️⃣</span>
                                    <strong>Service Day:</strong> Our professional team arrives at your location with all equipment
                                </li>
                                <li style="margin-bottom: 0; padding-left: 30px; position: relative;">
                                    <span style="position: absolute; left: 0; color: #f59e0b; font-weight: bold;">4️⃣</span>
                                    <strong>Enjoy:</strong> Your spotless, professionally cleaned car! ✨
                                </li>
                            </ul>
                        </div>
                    </div>
                    
                    <!-- Contact Information -->
                    <div style="background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%); padding: 30px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);">
                        <h4 style="color: #2563eb; margin: 0 0 20px 0; font-size: 20px; text-align: center;">
                            📞 Need to Contact Us?
                        </h4>
                        <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; margin-bottom: 20px;">
                            <a href="tel:{BUSINESS_PHONE}" style="display: inline-block; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 12px 25px; text-decoration: none; border-radius: 25px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);">
                                📞 {BUSINESS_PHONE}
                            </a>
                            <a href="mailto:{BUSINESS_EMAIL}" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 12px 25px; text-decoration: none; border-radius: 25px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);">
                                ✉️ Email Us
                            </a>
                        </div>
                        <table style="width: 100%; background: white; border-radius: 10px; padding: 20px; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 10px 0; font-weight: 600; color: #374151; width: 35%; font-size: 15px;">Service Area:</td>
                                <td style="padding: 10px 0; color: #1f2937; font-size: 15px;">Dubai, UAE (We come to you!)</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px 0; font-weight: 600; color: #374151; font-size: 15px;">Experience:</td>
                                <td style="padding: 10px 0; color: #1f2937; font-size: 15px;">{COMPANY_INFO['experience']} with {COMPANY_INFO['customers']} Happy Customers</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px 0; font-weight: 600; color: #374151; font-size: 15px;">Availability:</td>
                                <td style="padding: 10px 0; color: #1f2937; font-size: 15px;">7 Days a Week with Flexible Timing</td>
                            </tr>
                        </table>
                    </div>
                    
                    <!-- Important Notice -->
                    <div style="background: linear-gradient(135deg, #fef2f2 0%, #fef7f7 100%); padding: 25px; border-radius: 12px; border-left: 5px solid #ef4444; text-align: center; margin-bottom: 30px;">
                        <h4 style="color: #dc2626; margin: 0 0 15px 0; font-size: 18px;">
                            🚨 Important Notice
                        </h4>
                        <p style="color: #991b1b; margin: 0; font-weight: 600; font-size: 16px; line-height: 1.6;">
                            If you need to reschedule or have any questions, please call us immediately at 
                            <a href="tel:{BUSINESS_PHONE}" style="color: #dc2626; text-decoration: none; font-weight: 700;">{BUSINESS_PHONE}</a>
                        </p>
                    </div>
                    
                    <!-- Special Offers -->
                    <div style="background: linear-gradient(135deg, #f3e8ff 0%, #f5f3ff 100%); padding: 25px; border-radius: 12px; border-left: 5px solid #8b5cf6; text-align: center;">
                        <h4 style="color: #7c3aed; margin: 0 0 15px 0; font-size: 18px;">
                            🎁 Special Offers for You!
                        </h4>
                        <p style="color: #6d28d9; margin: 0 0 15px 0; font-weight: 600; font-size: 16px;">
                            Ask about our Monthly & Yearly packages for better savings!
                        </p>
                        <p style="color: #6d28d9; margin: 0; font-size: 14px;">
                            ✨ Yearly packages save you 30% | Monthly packages ensure consistent quality ✨
                        </p>
                    </div>
                </div>
                
                <!-- Footer -->
                <div style="background: #1f2937; color: white; padding: 40px 30px; text-align: center;">
                    <h3 style="margin: 0 0 15px 0; color: #4ade80; font-size: 24px;">Thank you for choosing {BUSINESS_NAME}! 🙏</h3>
                    <p style="margin: 0 0 20px 0; color: #d1d5db; font-size: 18px; font-weight: 500;">Professional Mobile Car Washing & Detailing Service</p>
                    <div style="margin: 25px 0;">
                        <p style="margin: 0; color: #9ca3af; font-size: 16px;">
                            📞 {BUSINESS_PHONE} | ✉️ {BUSINESS_EMAIL}
                        </p>
                        <p style="margin: 10px 0 0 0; color: #9ca3af; font-size: 16px;">
                            🌐 macmobilecarwash.com | 📍 Dubai, UAE
                        </p>
                    </div>
                    <div style="margin-top: 25px; padding-top: 25px; border-top: 1px solid #374151;">
                        <p style="margin: 0; color: #6b7280; font-size: 14px; line-height: 1.6;">
                            Follow us on social media for updates, tips, and special offers!<br>
                            We're committed to making your car look amazing every time! ✨
                        </p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        mail.send(msg)
        print(f"✅ Confirmation email sent successfully to {customer_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send confirmation email: {e}")
        return False

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Page not found',
        'message': 'The requested page does not exist.',
        'contact': BUSINESS_PHONE
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on our end. Please try again or contact us.',
        'contact': BUSINESS_PHONE
    }), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'error': 'Bad request',
        'message': 'Invalid request data provided.',
        'contact': BUSINESS_PHONE
    }), 400

# ==================== ADDITIONAL UTILITY ROUTES ====================

@app.route('/api/services')
def api_services():
    """API endpoint to get all services"""
    return jsonify({
        'success': True,
        'services': SERVICES,
        'features': SERVICE_FEATURES,
        'company': COMPANY_INFO
    })

@app.route('/api/testimonials')
def api_testimonials():
    """API endpoint to get testimonials"""
    return jsonify({
        'success': True,
        'testimonials': TESTIMONIALS
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': BUSINESS_NAME,
        'timestamp': datetime.now().isoformat()
    })

# ==================== MAIN APPLICATION ====================

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Print startup information
    print("=" * 60)
    print(f"🚗 {BUSINESS_NAME} - Flask Application Starting")
    print("=" * 60)
    print(f"📧 Business Email: {BUSINESS_EMAIL}")
    print(f"📞 Business Phone: {BUSINESS_PHONE}")
    print(f"📁 Data Directory: ./data/")
    print(f"💾 Bookings File: ./data/bookings.json")
    print("=" * 60)
    print("🌐 Server will start at: http://localhost:5000")
    print("🤖 Chatbot API: http://localhost:5000/api/chatbot")
    print("📞 Contact API: http://localhost:5000/api/contact")
    print("💰 Quote API: http://localhost:5000/api/quote")
    print("❤️  Health Check: http://localhost:5000/health")
    print("=" * 60)
    
    # Run the application
    app.run(
        debug=True, 
        host='0.0.0.0', 
        port=5000,
        threaded=True
    )
