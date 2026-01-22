# app/data.py

DESTINATIONS = {
    'everestbasecamp': {
        'id': '1',
        'name': 'Everest Base Camp',
        'hero_image': 'app/assets/images/ebc_hero.jpg',
        'temp': '-10°C to 5°C',
        'best_time': 'March - May',
        'altitude': '5,364m',
        'about': 'The ultimate pilgrimage for adventurers, standing at the foot of the world’s highest peak.',
        'radar_data': [100, 100, 40], # Adventure, Nature, Culture
        'lat_long': [28.0044, 86.8528],
        'culture': 'Deeply rooted Sherpa culture, prayer flags, and the spiritual Mani Rimdu festival.',
        'tradition_imgs': ['app/assets/images/ebc_trad1.jpg', 'app/assets/images/ebc_trad2.jpg'],
        'food': 'Sherpa Stew (Syakpa), Tibetan Bread, and high-energy Dal Bhat.',
        'food_imgs': ['app/assets/images/ebc_food1.jpg', 'app/assets/images/ebc_food2.jpg'],
        'intel': {
            'vibe': 'Extreme / Spiritual',
            'difficulty': 'High (Trek)',
            'stay': '12-14 Days',
            'transport': 'Helicopter / Foot'
        },
        'hotels': [
            {'name': 'Hotel Everest View', 'link': 'https://hoteleverestview.com/'},
            {'name': 'Yeti Mountain Home', 'link': 'https://www.yetimountainhome.com/'}
        ],
    },
    'pokharalakeside': {
        'id': '2',
        'name': 'Pokhara (Lakeside)',
        'hero_image': 'app/assets/images/annapurna.jpg',
        'temp': '15°C to 25°C',
        'best_time': 'Oct - Dec',
        'altitude': '822m',
        'about': 'A tranquil paradise where the Machhapuchhre peak reflects in the calm waters of Phewa Lake.',
        'radar_data': [90, 85, 60], 
        'lat_long': [28.2095, 83.9592],
        'culture': 'A fusion of hippie chill vibes and traditional Gurung hospitality.',
        'tradition_imgs': ['app/assets/images/stupa.jpeg', 'app/assets/images/phewa.jpeg'],
        'food': 'Fresh Lake Trout, Thakali Khana, and vibrant lakeside cafes.',
        'food_imgs': ['app/assets/images/selroti.jpeg', 'app/assets/images/food.jpeg'],
        'intel': {
            'vibe': 'Zen / Spiritual',
            'difficulty': 'Easy Access',
            'stay': '3-5 Days',
            'transport': 'Tuk-Tuk / Cycle'
        },
        'hotels': [
            {'name': 'Fish Tail Lodge', 'link': 'https://www.fishtail-lodge.com.np/'},
            {'name': 'Temple Tree Resort', 'link': 'https://www.templetreeresort.com/'}
        ],
    },
    # Add other entries using the same 'intel' and 'radar_data' structure
}