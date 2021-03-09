;; by Jiawei Liao 756560 
;; 1st May 2020
;; COMP90054-2020-SM1-a2
;; liao2@student.unimelb.edu

(define
    (problem pacman-level-1)
    (:domain pacman_hard)

;; problem map
;;  | 1 | 2 | 3 | 4 | 5 |
;; -|---|--- ---|---|---|
;; a| P | _ | _ | G | F |
;; b| C | _ | _ | G | _ |
;;  |---|---|---|---|---|

    (:objects
        G - Ghost
        F - Food
        C - Capsule
        E - Empty
        a1 a2 a3 a4 a5 b1 b2 b3 b4 b5 - cell
	)
	
	(:init
	    ;; initial position at a1
        (at a1)

        ;; initially not buffed by capsule
        (not (buffed2 C))
        (not (buffed1 C))
        
        ;; pacman can move between connected cells
        (connected a1 a2)
        (connected a1 b1)
        (connected a2 a1)
        (connected a2 b2)
        (connected a2 a3)
        (connected a3 a2)
        (connected a3 a4)
        (connected a3 b3)  
        (connected a4 a3)
        (connected a4 a5)
        (connected a4 b4)
        (connected a5 a4)
        (connected a5 b5)
        (connected b1 a1)
        (connected b1 b2)
        (connected b2 b1)
        (connected b2 b3)
        (connected b2 a2)
        (connected b3 b2)
        (connected b3 b4)
        (connected b3 a3)
        (connected b4 b3)
        (connected b4 b5)
        (connected b4 a4)
        (connected b5 b4)
        (connected b5 a5)
        
        ;; What is in a cell, e for empty, G for ghost, F for food
        (Incell a1 E)
        (Incell a2 E)
        (Incell a3 E)
        (Incell a4 G)
        (Incell a5 F)
        (Incell b1 E)
        (Incell b2 C)
        (Incell b3 E)
        (Incell b4 G)
        (Incell b5 C)
        
	)

    (:goal 
        (and
            ;; Goal achieved when 
            ;; 1. all food cells are cleared 
            (not (Incell a5 F))

            ;; 1. all ghosts cells are cleared
            (not (Incell a4 G))
            (not (Incell b4 G))
        )
	)
)