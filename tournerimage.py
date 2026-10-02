from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def eye_positions(img):
    # Affiche l'image et attend les clics; timeout=-1 signifie qu'il n'y a pas de limite de temps.
    plt.figure()
    plt.imshow(img)
    plt.axis('off')
    
    # Le premier clic donne les coordonnees (x, y) du premier point choisi.
    plt.title("Click 1")
    x1, y1 = plt.ginput(1, timeout=-1)[0]
    plt.plot(x1, y1, 'gx')
    plt.draw()
    
    # Le second clic donne les coordonnees du deuxieme point choisi.
    plt.title("Click 2")
    x2, y2 = plt.ginput(1, timeout=-1)[0]
    plt.plot(x2, y2, 'gx')
    plt.draw()
    plt.close()
    
    # Retourne les deux points; x augmente vers la droite et y vers le bas dans l'image.
    return (x1, y1), (x2, y2)

def extract_face(img):
    # Le traitement se fait en niveaux de gris ('L' = luminosite).
    gray_img = img.convert('L')
    
    # Demande les deux points qui serviront a calculer l'inclinaison.
    c1, c2 = eye_positions(gray_img)
    
    # atan2 calcule l'angle de la ligne entre les points; degrees le convertit en degres.
    angle = np.degrees(np.arctan2(c2[1] - c1[1], c2[0] - c1[0]))
    print("Angle =", angle)
    
    # Tourne l'image de cet angle. expand=False conserve la taille initiale du canevas,
    # donc les coins peuvent etre coupes apres la rotation.
    I2_img = gray_img.rotate(angle, expand=False)
    I2 = np.array(I2_img)

    # La rotation de Pillow se fait autour du centre de l'image. On applique donc
    # la meme rotation aux coordonnees des clics, relativement a ce centre.
    h, w = I2.shape
    R = np.array([[np.cos(np.radians(angle)), np.sin(np.radians(angle))],
                  [-np.sin(np.radians(angle)), np.cos(np.radians(angle))]])
    
    new_c1 = (R @ (np.array(c1).reshape(2, 1) - np.array([[w/2], [h/2]]))) + np.array([[w/2], [h/2]])
    new_c2 = (R @ (np.array(c2).reshape(2, 1) - np.array([[w/2], [h/2]]))) + np.array([[w/2], [h/2]])

    # Affiche l'image d'origine, puis les deux points repositionnes sur l'image tournee.
    plt.imshow(img, cmap='gray')
    
    # Les points verts permettent de verifier visuellement le resultat de la rotation.
    plt.figure()
    ax = plt.gca()
    ax.imshow(I2, cmap='gray')
    ax.plot(new_c1[0], new_c1[1], 'go')
    ax.plot(new_c2[0], new_c2[1], 'go')
    plt.title("Rotated image with eye positions (left, then right)")
    plt.show(block=False)
    
    plt.figure()
    
    # La distance entre les clics sert d'unite pour definir une decoupe proportionnelle.
    scale = np.sqrt(np.sum((new_c1 - new_c2) ** 2))

    # La boite Pillow est (gauche, haut, droite, bas). Ses dimensions et sa position
    # sont calculees autour du premier point, selon la distance entre les deux clics.
    x, y = new_c1.flatten()
    crop_box = (int(x - 0.5 * scale),
                int(y - 0.5 * scale),
                int(x + 1.5 * scale),
                int(y + 0.5 * scale))
    
    cropped = I2_img.crop(crop_box)
    # Active cette ligne pour obtenir une sortie de taille fixe (ici 200 x 200 pixels).
    # cropped = cropped.resize((200, 200))

    # Affiche la decoupe avant de la retourner a la fonction appelante.
    plt.imshow(cropped, cmap='gray')
    plt.axis('off')
    plt.show(block=False)

    return cropped


if __name__ == "__main__":
    # Point d'entree du programme: ouvre l'image, lance le traitement et affiche le resultat.
    img = Image.open('2.jpg')
    # left, right = eye_positions(img)
    # print("Left eye: (%.1f, %.1f)" % left)
    # print("Right eye: (%.1f, %.1f)" % right)
    face = extract_face(img)
    plt.figure()
    plt.imshow(face, cmap='gray')
    plt.title("Extracted Face")
    plt.show()
