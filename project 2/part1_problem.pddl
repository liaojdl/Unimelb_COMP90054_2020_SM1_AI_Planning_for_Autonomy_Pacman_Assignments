;; by Jiawei Liao 756560 
;; 1st May 2020
;; COMP90054-2020-SM1-a2
;; liao2@student.unimelb.edu

(define
    (problem pacman-level-1)
    (:domain pacman_simple)

;; problem map
;;  | 1 | 2 | 3 |
;; -|---|---|---|
;; a| P | G | F | 
;; b| _ | _ | _ | 
;;  |---|---|---| 


    (:objects
        G - Ghost
        F - Food
        E - Empty
        a1 a2 a3 b1 b2 b3 - cell
	)
	
	(:init
	    ;; initial position at a1
        (at a1)
        
        ;; pacman can move between connected cells
        (connected a1 a2)
        (connected a1 b1)
        (connected a2 a1)
        (connected a2 b2)
        (connected a2 a3)
        (connected a3 a2)
        (connected a3 b3)
        (connected b1 a1)
        (connected b1 b2)
        (connected b2 b1)
        (connected b2 a2)
        (connected b2 b3)
        (connected b3 b2)
        (connected b3 a3)
        
        ;; What is in a cell, e for empty, G for ghost, F for food
        (Incell a1 E)
        (Incell a2 G)
        (Incell a3 F)
        (Incell b1 E)
        (Incell b2 E)
        (Incell b3 E)
	)

    (:goal 
        (and
            ;; Goal achieved when all food cells are cleared to empty cells
            (not (Incell a3 F))
        )
	)
)