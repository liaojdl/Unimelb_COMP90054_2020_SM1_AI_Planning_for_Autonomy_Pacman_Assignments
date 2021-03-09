;; by Jiawei Liao 756560 
;; 1st May 2020
;; COMP90054-2020-SM1-a2
;; liao2@student.unimelb.edu

(define
    (domain pacman_simple)
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
    )


    (:action move
        :parameters (?cell1 ?cell2 - cell) 
        ;; can only move to cell2 if cell1 and cell 2 are connected
        ;; Forbit move if cell2 has Ghost
        :precondition (and 
            (at ?cell1 )
            (connected ?cell1 ?cell2)
            (exists (?G - Ghost) 
                (and (not (Incell ?cell2 ?G)))
            )   
        )
        ;; once reached cell 2, consumes the object inside cell2
        ;; changes cell2 to empty
        :effect (and 
            (at ?cell2)
            (not (at ?cell1))
            (forall (?con - consumable_object)
                (forall (?E - Empty)
                    (when (and (Incell ?cell2 ?con))
                        (and (Incell ?cell2 ?E) (not (Incell ?cell2 ?con)))
                    )
                )    
            )
        )
    )
)