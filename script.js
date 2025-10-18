document.addEventListener('DOMContentLoaded', () => {

    const appContent = document.getElementById('app-content');
    const navLinks = document.querySelectorAll('.nav-links a');

    // --- UPDATED: Mock Data with realistic room images ---
    const rooms = [
        { id: 101, type: 'Single Room', capacity: 1, available: true, price: 5000, img: 'https://images.unsplash.com/photo-1618221614943-5a3a25d0c7a6?q=80&w=2070&auto=format&fit=crop' },
        { id: 201, type: 'Double Room', capacity: 2, available: true, price: 3500, img: 'https://images.unsplash.com/photo-1560185893-a5536c80e6cb?q=80&w=2070&auto=format&fit=crop' },
        { id: 301, type: 'Triple Room', capacity: 3, available: false, price: 2500, img: 'https://images.unsplash.com/photo-1595526114035-0d45ed16433d?q=80&w=2070&auto=format&fit=crop' },
        { id: 102, type: 'Single Room', capacity: 1, available: false, price: 5200, img: 'https://images.unsplash.com/photo-1585412399212-9171b38f1267?q=80&w=1935&auto=format&fit=crop' },
        { id: 202, type: 'Double Room', capacity: 2, available: true, price: 3800, img: 'https://images.unsplash.com/photo-1566647970335-d3ba88a53123?q=80&w=1974&auto=format&fit=crop' },
        { id: 302, type: 'Triple Room', capacity: 3, available: true, price: 2800, img: 'https://images.unsplash.com/photo-1598605272254-cd61a8b7d996?q=80&w=2070&auto=format&fit=crop' },
    ];

    // --- Page Templates with all your requested changes ---
    const pages = {
        home: `
            <div class="bg-white rounded-lg shadow-md p-8 text-center">
                <h1 class="text-4xl font-bold text-gray-800">Welcome to HostelSys</h1>
                <p class="mt-4 text-lg text-gray-600">The easiest way to find and book your student accommodation. Your next home is just a few clicks away!</p>
                <div class="mt-8">
                    <a href="#" data-page-link="rooms" class="bg-blue-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-blue-700 transition duration-300">Find My Room</a>
                </div>
            </div>
        `,
        // --- UPDATED: Login form with Username and Password ---
        login: `
            <div class="max-w-md mx-auto bg-white rounded-lg shadow-md p-8">
                <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Login</h2>
                <form>
                    <div class="mb-4">
                        <label for="username" class="block text-gray-700 font-medium mb-2">Username</label>
                        <input type="text" id="username" name="username" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required />
                    </div>
                    <div class="mb-6">
                        <label for="password" class="block text-gray-700 font-medium mb-2">Password</label>
                        <input type="password" id="password" name="password" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required />
                    </div>
                    <button type="submit" class="w-full bg-blue-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700 transition duration-300">Login</button>
                </form>
            </div>
        `,
        // --- UPDATED: Register form with Name, Phone, Gmail, Password ---
        register: `
             <div class="max-w-md mx-auto bg-white rounded-lg shadow-md p-8">
                <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Create an Account</h2>
                <form>
                    <div class="mb-4">
                        <label for="name" class="block text-gray-700 font-medium mb-2">Full Name</label>
                        <input type="text" id="name" name="name" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required />
                    </div>
                    <div class="mb-4">
                        <label for="phone" class="block text-gray-700 font-medium mb-2">Phone Number</label>
                        <input type="tel" id="phone" name="phone" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required />
                    </div>
                    <div class="mb-4">
                        <label for="email" class="block text-gray-700 font-medium mb-2">Gmail</label>
                        <input type="email" id="email" name="email" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required />
                    </div>
                    <div class="mb-6">
                        <label for="password" class="block text-gray-700 font-medium mb-2">Password</label>
                        <input type="password" id="password" name="password" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required />
                    </div>
                    <button type="submit" class="w-full bg-blue-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700 transition duration-300">Register</button>
                </form>
            </div>
        `,
        // --- UPDATED: Room list with real images and prices ---
        rooms: `
            <h2 class="text-3xl font-bold text-gray-800 mb-8 text-center">Our Rooms</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                ${rooms.map(room => `
                    <div class="bg-white rounded-lg shadow-lg overflow-hidden transform hover:-translate-y-2 transition-transform duration-300">
                        <img src="${room.img}" alt="${room.type}" class="w-full h-56 object-cover">
                        <div class="p-6">
                            <h3 class="text-2xl font-bold text-gray-800">${room.type}</h3>
                            <p class="text-gray-600 mt-2">Capacity: ${room.capacity} Student(s)</p>
                            <p class="text-3xl font-bold text-blue-600 mt-4">₹${room.price}<span class="text-lg font-normal text-gray-500">/month</span></p>
                            <div class="mt-6">
                                ${room.available 
                                    ? `<button class="w-full bg-blue-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700 transition duration-300">Book Now</button>` 
                                    : `<div class="w-full bg-red-500 text-white font-bold py-2 px-4 rounded-lg text-center">Booked</div>`
                                }
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `
    };

    // --- Router Logic (no changes needed here) ---
    const navigate = (page) => {
        appContent.innerHTML = pages[page];
        const dynamicLinks = appContent.querySelectorAll('[data-page-link]');
        dynamicLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const pageName = e.target.getAttribute('data-page-link');
                navigate(pageName);
            });
        });
    };

    navLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const page = event.target.getAttribute('data-page');
            if (page) {
                navigate(page);
            }
        });
    });

    // --- Initial Page Load ---
    navigate('home');
});