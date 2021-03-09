;; by Jiawei Liao 756560 
;; 1st May 2020
;; COMP90054-2020-SM1-a2
;; liao2@student.unimelb.edu

(define
    (domain pacman_mid)
    (:requirements :strips :typing :equality :adl)


    (:types
        physical_object location - object
        consumable_object Empty - physical_object
        Ghost Food Capsule - consumable_object
        cell - location
    )
    
    (:predicates
        ;; move from one cell to another
        (move ?from ?to - cell)
        ;; the location of Pacman
        (at ?loc - cell)
        ;; two connected cells are next to each other (left,right,top,bottom)
        (connected ?from ?to - cell)
        ;; What is the the cell, either food, ghost or empty
        (Incell ?loc - cell ?obj - physical_object)
        ;; whether the player is buffed by capsule
        (buffed ?C - Capsule)
    )

    (:action move
        :parameters (?cell1 ?cell2 - cell) 
        :precondition (and
            ;; can only move to cell2 if cell1 and cell 2 are connected 
            (at ?cell1 )
            (connected ?cell1 ?cell2)
            (or 
                ;; only permits move to cell with ghost if buffed by capsule
                (exists (?G - Ghost) 
                    (exists (?C - Capsule)
                        (and (Incell ?cell2 ?G) (buffed ?C) )
                    )
                )
                
                (exists (?G - Ghost) 
                    (and (not (Incell ?cell2 ?G)))
                )  
            )  
        )
        :effect (and 
            (at ?cell2)
            (not (at ?cell1))
            ;; 1. clears original consumable object in cell2 to empty
            (forall (?con - consumable_object) 
                (forall (?E - Empty)
                    (when (and (Incell ?cell2 ?con))
                        (and (Incell ?cell2 ?E) (not (Incell ?cell2 ?con)))
                    )
                )    
            )
            ;; 2. Capsule: activate the buff to eat ghosts
            (forall (?C - Capsule) 
                (when (and (Incell ?cell2 ?C))
                    (and (buffed ?C))
                )  
            )
        )
    )
)