import numpy as np

def compute_k_factors(L, v):
    #L: features --> properties --> LEN_PRED
    #v: features --> properties --> SOG
    k_AD = L * np.exp(0.3591 * np.log(v) + 0.0952)
    k_DT = L * np.exp(0.5441 * np.log(v) - 0.0795)
    return k_AD, k_DT

def compute_R_factors(L, k_AD, k_DT, s):
    R_fore = (L + (1 + s) * 0.67 * np.sqrt(k_AD**2 + (k_DT / 2)**2))
    R_aft = (L + 0.67 * np.sqrt(k_AD**2 + (k_DT / 2)**2))
    R_starb = (0.2 + k_DT) / L
    R_port = (0.2 + 0.75 * k_DT) / L
    return R_fore, R_aft, R_starb, R_port

def calculate_alpha(own_ship_position, target_ship_position, own_ship_cog):
    #own_ship_position: features --> geometry --> coordinates
    #target_ship_position: features --> geometry --> coordinates
    #own_ship_cog: features --> 'COG'
    dx = target_ship_position[0] - own_ship_position[0]
    dy = target_ship_position[1] - own_ship_position[1]
    alpha = np.arctan2(dy, dx) - own_ship_cog
    return alpha

def create_ellipse(L, v, vt, own_ship_position, target_ship_position, own_ship_cog, mode='head_on'):
    #own_ship_position: features --> geometry --> coordinates
    #target_ship_position: features --> geometry --> coordinates
    #own_ship_cog: features --> 'COG'
    
    #참고: target_ship_position은 타원을 생성하는데 직접적으로 쓰인다기보다는, s값을 계산하는데에 쓰임!!
    k_AD, k_DT = compute_k_factors(L, v)
    
    alpha = calculate_alpha(own_ship_position, target_ship_position, own_ship_cog)
    
    # Determine s based on mode
    if mode == 'head_on':
        s = 2 - (v - vt) / v
    elif mode == 'crossing':
        s = 2 - alpha / np.pi
    elif mode == 'overtaking':
        s = 1
    else:
        raise ValueError("Invalid mode. Choose from 'head_on', 'crossing', or 'overtaking'.")
    
    R_fore, R_aft, R_starb, R_port = compute_R_factors(L, k_AD, k_DT, s)

    a = (abs(R_fore) + abs(R_aft)) / 2
    b = (abs(R_starb) + abs(R_port)) / 2
    
    delta_a = abs(R_fore) - a
    delta_b = abs(R_starb) - b
    
    ellipse = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[]]
        },
        "properties": {
            "angle": 0  
        }
    }
    
    num_points = 100
    for i in range(num_points):
        theta = 2.0 * np.pi * float(i) / float(num_points)
        x = a * np.cos(theta)
        y = b * np.sin(theta)
        ellipse["geometry"]["coordinates"][0].append([
            x - delta_a,
            y - delta_b
        ])
    ellipse["geometry"]["coordinates"][0].append(ellipse["geometry"]["coordinates"][0][0]) 
    
    return ellipse



